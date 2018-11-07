from app.audio import Audio

class AppController:

    # Audio Settings
    audio_channels_in = 6
    audio_channels_out = 8
    audio_device_in = 9
    audio_device_out = 9
    audio_samplerate = 44100
    audio_buffersize = 256

    def __init__(self, view):
        # Initialize App Window
        self.view = view(self) # AppView(self)
        self.initial_view()

        # Initialize Audio
        self.audio = Audio(self, self.audio_device_in, self.audio_device_out, self.audio_samplerate, self.audio_buffersize)
        self.audio.start()

    def run(self):
        self.view.run()

    def initial_view(self):
        self.view.update_state('none')

        levels = {'input': [], 'output': []}
        max_levels = {'input': [], 'output': []}
        for i in range(0, self.audio_channels_in):
            levels['input'].append(float(i + 1) / float(self.audio_channels_in + 1))
            max_levels['input'].append(float(i + 1) / float(self.audio_channels_in))
        for i in range(0, self.audio_channels_out):
            levels['output'].append(float(i + 1) / float(self.audio_channels_out + 1))
            max_levels['output'].append(float(i + 1) / float(self.audio_channels_out))

        self.view.update_levels(levels, max_levels)

    # Audio Wrapper Methods

    def play(self):
        return self.audio.play()

    def pause(self):
        return self.audio.pause()

    def stop(self):
        return self.audio.stop()

    def record(self):
        return self.audio.record()

    # Audio Events

    def state_update(self, state):
        self.view.update_state(state)

    def audio_update(self, avg_levels, max_levels):
        self.view.update_levels(avg_levels, max_levels)

    # Window Methods

    def update(self):
        self.view.update()

    def destroy(self):
        # Deinitialize Audio
        self.audio.destroy()
        self.view.destroy()
