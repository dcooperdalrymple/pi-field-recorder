#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pi Field Recorder: Battery-operated field recorder designed for use with the Audio Injector Octo and piTFT touch screen.

import urwid
from audio import Audio

class AppView(urwid.WidgetWrap):
    # Color Palette
    palette = [
        ('window', 'light green', 'black'),
        ('label', 'light green', 'black'),
        ('alt label', 'white', 'black'),
        ('inv label', 'black', 'light green'),
        ('button normal', 'light green', 'black'),
        ('button select', 'yellow', 'black'),
        ('button active', 'light red', 'black'),
        ('button disabled', 'dark green', 'black'),
        ('meter low', 'black', 'dark green'),
        ('meter low smooth', 'dark green', 'black'),
        ('meter high', 'black', 'light green'),
        ('meter high smooth', 'light green', 'black'),
    ]

    # Frames
    window_width = 320
    window_height = 240

    controls_height = 96
    meters_height = 144

    # Buttons
    button_width = 64
    button_height = 64

    def __init__(self, controller):
        self.controller = controller
        urwid.WidgetWrap.__init__(self, self.main_window())

    # GUI Elements

    def meters_control(self):
        satt = {(1, 0): 'meter low smooth', (2, 0): 'meter high smooth'}
        w = urwid.BarGraph(['bg', 'meter low', 'meter high'], satt=satt)
        return w

    def button_control(self, text, action=None):
        w = AppButton(text, self.on_button, action)
        w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 1))
        w = urwid.AttrMap(w, 'button disabled', 'button disabled')
        return w

    def label_control(self, text):
        w = urwid.Text(text, align='center')
        w = urwid.AttrMap(w, 'label')
        return w

    def set_button(self, w, state):
        if state == 'normal':
            w.set_attr_map({None: 'button normal'})
            w.set_focus_map({None: 'button select'})
        elif state == 'active':
            w.set_attr_map({None: 'button active'})
            w.set_focus_map({None: 'button select'})
        elif state == 'disabled':
            w.set_attr_map({None: 'button disabled'})
            w.set_focus_map({None: 'button dissabled'})

    # Window/Widgets

    def main_window(self):
        controls = self.build_controls()
        meters = self.build_meters()

        # Wrap controls
        w = urwid.Frame(meters, header=controls)
        w = urwid.AttrMap(w, 'window')
        return w

    def build_controls(self):
        self.play_button = self.button_control(u'Play', 'play')
        self.pause_button = self.button_control(u'Pause', 'pause')
        self.stop_button = self.button_control(u'Stop', 'stop')
        self.record_button = self.button_control(u'Record', 'record')

        w = urwid.Columns([self.play_button, self.pause_button, self.stop_button, self.record_button])
        w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 1))
        w = urwid.Pile([urwid.Divider(), w, urwid.Divider()])
        return w

    def build_meters(self):
        self.input_meters = self.meters_control()
        self.output_meters = self.meters_control()

        input_frame = urwid.Frame(urwid.WidgetWrap(self.input_meters), header=self.build_meter_title(u'Inputs'), footer=self.build_meter_labels(self.controller.audio_channels_in))
        input_frame = urwid.LineBox(input_frame)

        output_frame = urwid.Frame(urwid.WidgetWrap(self.output_meters), header=self.build_meter_title(u'Outputs'), footer=self.build_meter_labels(self.controller.audio_channels_out))
        output_frame = urwid.LineBox(output_frame)

        w = urwid.Columns([input_frame, output_frame])
        return w

    def build_meter_title(self, title):
        w = self.label_control(title)
        w.set_attr_map({None: 'inv label'})
        w = urwid.Pile([w, urwid.Divider()])
        return w

    def build_meter_labels(self, count):
        l = []
        for i in range(0, count):
            l.append(self.label_control(str(i + 1)))

        w = urwid.Columns(l)
        w = urwid.Pile([urwid.Divider(), w])
        return w

    # Update Events

    def update_state(self, state):
        if state == 'play':
            self.set_button(self.play_button, 'active')
            self.set_button(self.pause_button, 'normal')
            self.set_button(self.stop_button, 'normal')
            self.set_button(self.record_button, 'disabled')
        elif state == 'play_pause':
            self.set_button(self.play_button, 'active')
            self.set_button(self.pause_button, 'active')
            self.set_button(self.stop_button, 'normal')
            self.set_button(self.record_button, 'disabled')
        elif state == 'record':
            self.set_button(self.play_button, 'disabled')
            self.set_button(self.pause_button, 'normal')
            self.set_button(self.stop_button, 'normal')
            self.set_button(self.record_button, 'active')
        elif state == 'record_pause':
            self.set_button(self.play_button, 'disabled')
            self.set_button(self.pause_button, 'active')
            self.set_button(self.stop_button, 'normal')
            self.set_button(self.record_button, 'active')
        elif state == 'none':
            self.set_button(self.play_button, 'normal')
            self.set_button(self.pause_button, 'disabled')
            self.set_button(self.stop_button, 'disabled')
            self.set_button(self.record_button, 'normal')
        else:
            return False

        return True

    def update_levels(self, levels, max_levels):
        input_data = []
        for i in range(0, min(self.controller.audio_channels_in, len(levels['input']))):
            input_data.append([max_levels['input'][i], levels['input'][i]])

        output_data = []
        for i in range(0, min(self.controller.audio_channels_out, len(levels['output']))):
            output_data.append([max_levels['output'][i], levels['output'][i]])

        self.input_meters.set_data(input_data, 1.0)
        self.output_meters.set_data(output_data, 1.0)

        return True

    # Button Events

    def on_button(self, w, action):
        if action == 'play':
            self.controller.play()
        elif action == 'pause':
            self.controller.pause()
        elif action == 'stop':
            self.controller.stop()
        elif action == 'record':
            self.controller.record()

class AppController:

    # Audio Settings
    audio_channels_in = 6
    audio_channels_out = 8

    def __init__(self):
        # Initialize Audio
        self.audio = Audio(self, 0, 0, 44100, 256)
        self.audio.start()

        # Initialize App Window
        self.view = AppView(self)
        self.initial_view()

    def run(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=self.key_input)
        self.loop.run()

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

    def key_input(self, key):
        if key in ('q', 'Q', 'esc'):
            self.exit()

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
        self.loop.draw_screen()

    def exit(self):
        # Deinitialize Audio
        self.audio.destroy()

        # Stop Urwid Loop
        raise urwid.ExitMainLoop()

class AppButton(urwid.WidgetWrap):
    _border_char = u'─'
    def __init__(self, label, on_press=None, user_data=None):
        min_width = 12
        padding_size = (min_width - len(label)) / 2
        if padding_size < 0:
            padding_size = 0

        border = self._border_char * (len(label) + padding_size * 2)
        cursor_position = len(border) + padding_size

        self.top = u'┌' + border + u'┐\n'
        self.middle = u'│' + (u' ' * padding_size) + label + (u' ' * padding_size) + u'│\n'
        self.bottom = u'└' + border + u'┘'

        self.widget = urwid.Pile([
            urwid.Text(self.top[:-1]),
            urwid.Text(self.middle[:-1]),
            urwid.Text(self.bottom),
        ])

        # Hidden button hack
        self._hidden_button = urwid.Button('hidden %s' % label, on_press, user_data)

        super(AppButton, self).__init__(self.widget)

    def selectable(self):
        return True

    def keypress(self, *args, **kw):
        return self._hidden_button.keypress(*args, **kw)

    def mouse_event(self, *args, **kw):
        return self._hidden_button.mouse_event(*args, **kw)

def main():
    AppController().run()

if __name__ == '__main__':
    main()
