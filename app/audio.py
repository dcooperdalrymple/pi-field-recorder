# Threading Libraries
import time
import threading

# Audio Libraries
import sounddevice
import soundfile

# Data Libraries
import numpy
assert numpy
import math

class Audio(threading.Thread):
    # Default Device Settings
    log_offset = 0.1
    log_scale = 0.96025
    avg_time = 0.25
    max_time = 1.0

    def __init__(self, parent, in_device=0, out_device=0, samplerate=False, blocksize=False):
        self.parent = parent
        super(Audio, self).__init__()

        # Query Devices
        self._print_devices()

        self.in_device = in_device
        in_device_info = sounddevice.query_devices(self.in_device, 'input')
        self._print_device_info('Input Device', in_device_info)

        self.out_device = out_device
        out_device_info = sounddevice.query_devices(self.out_device, 'output')
        self._print_device_info('Output Device', out_device_info)

        # Device Settings
        self.data_type = 'float32'
        self.channels = min(in_device_info['max_input_channels'], out_device_info['max_output_channels'])
        self.latency = min(in_device_info['default_low_input_latency'], out_device_info['default_low_output_latency'])
        self.samplerate = min(in_device_info['default_samplerate'], out_device_info['default_samplerate'])
        if samplerate != False:
            self.samplerate = samplerate
        self.blocksize = int(float(self.samplerate) * self.latency)
        if blocksize != False:
            self.blocksize = blocksize

        self._print_configuration()

        # Audio Thread Settings
        self._state = 'none' # 'none', 'play', 'play_pause', 'record', 'record_pause'
        self._passthrough = True
        self._mixdown = True
        self._destroy = False

        # Initialize Level Arrays
        self._levels = { 'input': False, 'output': False }
        self._levels['input'] = [0.0 for i in range(0, self.channels)]
        self._levels['output'] = [0.0 for i in range(0, self.channels)]

        # Setup moving average arrays
        self._avg_blocksize = int(math.floor((self.avg_time * self.samplerate) / self.blocksize)) # Calculate number of block frames
        self._max_blocksize = int(math.floor((self.max_time * self.samplerate) / self.blocksize))
        self._max_interval = 1.0 / float(self._max_blocksize)

        self._avg_blocks = { 'input': False, 'output': False }
        self._avg_blocks['input'] = numpy.full((self.channels, self._avg_blocksize), 0.0)
        self._avg_blocks['output'] = numpy.full((self.channels, self._avg_blocksize), 0.0)

        self._avg_levels = { 'input': False, 'output': False }
        self._avg_levels['input'] = [0.0 for i in range(0, self.channels)]
        self._avg_levels['output'] = [0.0 for i in range(0, self.channels)]

        self._max_levels = { 'input': False, 'output': False }
        self._max_levels['input'] = [0.0 for i in range(0, self.channels)]
        self._max_levels['output'] = [0.0 for i in range(0, self.channels)]

    # Properties

    def get_state(self):
        return self._state

    def set_state(self, state='none'):
        #if self._state == state:
        #    return False
        self._state = state
        self.parent.state_update(self._state)
        return True

    def set_passthrough(self, passthrough=True):
        self._passthrough = passthrough
        return True

    def get_passthrough(self):
        return self._passthrough

    def set_mixdown(self, mixdown=True):
        self._mixdown = mixdown
        return True

    def get_mixdown(self):
        return self._mixdown

    def get_levels(self):
        return self._levels

    # Methods

    def play(self):
        if self._state == 'none' or self._state == 'play_pause' or self._state == 'record_pause':
            if self._state == 'none' or self._state == 'play_pause':
                self.set_state('play')
            elif self._state == 'record_pause':
                self.set_state('record')
        else:
            return False

        return True

    def record(self):
        if self._state != 'none':
            return False

        self.set_state('record')

        return False

    def pause(self):
        if self._state == 'none':
            return False

        if self._state == 'play':
            self.set_state('play_pause')
        elif self._state == 'play_pause':
            self.set_state('play')
        elif self._state == 'record':
            self.set_state('record_pause')
        elif self._state == 'record_pause':
            self.set_state('record')

        return True

    def stop(self):
        if self._state == 'none':
            return False
        self.set_state('none')
        return False

    def load_play(self, filepath):
        return False

    def load_record(self, filepath):
        return False

    def destroy(self):
        self._destroy = True

    # Audio Thread

    def _audio_callback(self, indata, outdata, frames, time, status):
        if self._destroy == True:
            return

        if status:
            print(status)

        # Audio Pass-Through
        if self._passthrough == True:
            if self._mixdown == True and self.channels >= 2: # Mix down audio to stereo
                outdata[:, 0] = self._calculate_mix(indata[:, ::2]) # Left/even channels
                outdata[:, 1] = self._calculate_mix(indata[:, 1::2]) # Right/odd channels
            else:
                outdata[:] = indata

        if indata.any():
            for i in range(0, self.channels):
                inchandata = indata[:, i]
                self._levels['input'][i] = self._calculate_level(inchandata)

        if outdata.any():
            for i in range(0, self.channels):
                outchandata = outdata[:, i]
                self._levels['output'][i] = self._calculate_level(outchandata)

        # Calculate Averages
        self._calculate_averages('input')
        self._calculate_averages('output')

        # Calculate Maxes
        self._calculate_maxes('input')
        self._calculate_maxes('output')

        self.parent.audio_update(self._avg_levels, self._max_levels)

    def _calculate_level(self, data):
        linear = numpy.max(numpy.abs(data))
        log = (math.log(linear + self.log_offset, 10) + 1.0) * self.log_scale
        return log

    def _calculate_averages(self, device='input'):
        self._avg_blocks[device] = numpy.roll(self._avg_blocks[device], 1)
        for i in range(0, self.channels):
            self._avg_blocks[device][i,0] = self._levels[device][i]
            self._avg_levels[device][i] = numpy.average(self._avg_blocks[device][i])

    def _calculate_maxes(self, device='input'):
        for i in range(0, self.channels):
            max_level = numpy.max(self._avg_blocks[device][i])
            if max_level > self._max_levels[device][i]:
                self._max_levels[device][i] = max_level
            elif max_level < self._max_levels[device][i]:
                self._max_levels[device][i] = max(self._max_levels[device][i] - self._max_interval, 0.0)

    def _calculate_mix(self, data):
        if numpy.shape(data)[1] <= 1:
            return data[:, 0]

        mix = data[:, 0]
        for i in range(0, numpy.shape(data)[0]):
            for j in range(1, numpy.shape(data)[1]):
                mix[i] = self.__calculate_mix(mix[i], data[i, j])

        return mix

    def __calculate_mix(self, a, b):
        if a < 0.0 and b < 0.0:
            return (a + b) - (a * b / -1.0)
        elif a > 0.0 and b > 0.0:
            return (a + b) - (a * b / 1.0)
        else:
            return a + b

    def run(self):
        self.set_state('none') # Send initial state update

        print(':: Starting Audio Stream ::')
        with sounddevice.Stream(device=(self.in_device, self.out_device), samplerate=self.samplerate, blocksize=self.blocksize, dtype=self.data_type, channels=self.channels, latency=self.latency, callback=self._audio_callback):
            while True:
                if self._destroy == True:
                    break
        print(':: Ending Audio Stream ::')

    # Device Information Debugging

    def _print_devices(self):
        print(':: Available Devices ::')
        print(sounddevice.query_devices())
        print('')

    def _print_device_info(self, title, device_info):
        print(":: %s ::" % title)
        info = {
            'Name': device_info['name'],
            'Input Channels': device_info['max_input_channels'],
            'Output Channels': device_info['max_output_channels'],
            'Sample Rate': device_info['default_samplerate'],
            'Input Latency': "%s => %s" % (device_info['default_low_input_latency'], device_info['default_high_input_latency']),
            'Output Latency': "%s => %s" % (device_info['default_low_output_latency'], device_info['default_high_output_latency']),
        }
        for key, value in info.iteritems():
            print("%s: %s" % (key, value))
        print('')

    def _print_configuration(self):
        print(':: Current Configuration ::')
        info = {
            'Channels': self.channels,
            'Sample Rate': self.samplerate,
            'Buffer Size': self.blocksize,
            'Latency': self.latency,
        }
        for key, value in info.iteritems():
            print("%s: %s" % (key, value))
        print('')
