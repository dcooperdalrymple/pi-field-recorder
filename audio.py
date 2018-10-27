import os
import time
import threading
import pyaudio
import wave

class PiFieldRecorderAudio(threading.Thread):
    def __init__(self, device_index=1, channels_in=6, channels_out=8, buffersize=4096, format = pyaudio.paInt24, samplerate=48000):
        super(PiFieldRecorderAudio, self).__init__()

        # Set parameters
        self.device_index = device_index
        self.channels_in = channels_in
        self.channels_out = channels_out
        self.buffersize = buffersize
        self.format = format
        self.samplerate = samplerate

        # Set Audio State
        self.state = 'none' # 'none', 'play', 'play_pause', 'record', 'record_pause'
        self._destroy = False

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

    def get_state(self):
        return self.state

    def play(self, filename):
        if (self.state != 'none') return False
        self.state = 'play'

        self._stop_stream()

    def record(self, filename):


    def stop(self):
        self.active = False
        time.sleep(0.1)

    def load(self, filepath):
        if self.active == True
            self.stop()
        self.filepath = os.path.abspath(filepath)

    def destroy(self):
        self._stop_stream()
        self.audio.terminate()

    def run(self):

        # Initialize stream by opening audio device
        self.stream = self.audio.open(input_device_index=self.device_index, channels=self.channels_in, frames_per_buffer=self.buffersize, format=self.format rate=self.samplerate, input=True)

        while self._destroy == False
            


    def _stop_stream(self):
        if self.stream != None
            self.stream.stop_stream()
            self.stream.close()
        self.stream = None
