#!/usr/bin/env python

# Pi Field Recorder: Battery-operated field recorder designed for use with the Audio Injector Octo and piTFT touch screen.

from Tkinter import *
import Tkinter

from audio import PiFieldRecorderAudio
import numpy
assert numpy

class PiFieldRecorderApp:
    # Frames
    window_width = 320
    window_height = 240
    window_bg = '#000000'

    controls_height = 96
    controls_bg = '#000000'

    meters_height = 144
    meters_bg = '#000000' # '#181818'
    meters_inputs_width = 140
    meters_outputs_width = 180

    # Labels
    label_fg = '#00a400' # '#ffffff'
    label_font_family = 'Monospace'
    label_font_size = 12
    label_font_size_small = 8
    label_font_size_large = 16

    # Buttons
    button_width = 64
    button_height = 64
    button_fg = '#00a400'
    button_active_fg = '#00e400'

    # Meters
    meter_label = 18
    meter_sublabel = 16
    meter_height = 96
    meter_width = 16
    meter_border = 1
    meter_color = '#00a400'

    # Audio Settings
    audio_channels_in = 6
    audio_channels_out = 8

    def __init__(self, master):

        # Load Assets
        self.img_button_play = PhotoImage(file="./assets/button-play.gif")
        self.img_button_play_active = PhotoImage(file="./assets/button-play-active.gif")
        self.img_button_play_inactive = PhotoImage(file="./assets/button-play-inactive.gif")
        self.img_button_record = PhotoImage(file="./assets/button-record.gif")
        self.img_button_record_active = PhotoImage(file="./assets/button-record-active.gif")
        self.img_button_record_inactive = PhotoImage(file="./assets/button-record-inactive.gif")
        self.img_button_pause = PhotoImage(file="./assets/button-pause.gif")
        self.img_button_pause_active = PhotoImage(file="./assets/button-pause-active.gif")
        self.img_button_pause_inactive = PhotoImage(file="./assets/button-pause-inactive.gif")
        self.img_button_stop = PhotoImage(file="./assets/button-stop.gif")
        self.img_button_stop_active = PhotoImage(file="./assets/button-stop-active.gif")
        self.img_button_stop_inactive = PhotoImage(file="./assets/button-stop-inactive.gif")

        # Set up window
        self.master = master
        self.master.title('Pi Field Recorder')
        self.master.geometry(str(self.window_width) + 'x' + str(self.window_height))
        self.master.resizable(0, 0)
        self.master.configure(background=self.window_bg)
        self.master.bind('<Destroy>', self._destroy)

        # Configure control frame
        self.controls_frame = Frame(master, bg=self.controls_bg, width=self.window_width, height=self.controls_height)
        self.controls_frame.place(relx=0, rely=0, anchor='nw', x=0, y=0)

        # Configure and place buttons
        padding_button = (self.window_width - self.button_width * 4) / 5;
        posy = (self.controls_height - self.button_height) / 2

        posx = padding_button
        self.play_button = Button(master=self.controls_frame, command=self.play, background=self.button_fg, foreground=self.controls_bg, activebackground=self.button_fg, activeforeground=self.controls_bg, image=self.img_button_play, border='0', borderwidth=0, highlightthickness=0, relief=FLAT, width=self.button_width, height=self.button_height)
        self.play_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')

        posx += self.button_width + padding_button
        self.pause_button = Button(master=self.controls_frame, command=self.pause, background=self.button_fg, foreground=self.controls_bg, activebackground=self.button_fg, activeforeground=self.controls_bg, image=self.img_button_pause, border='0', borderwidth=0, highlightthickness=0, relief=FLAT, width=self.button_width, height=self.button_height)
        self.pause_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')

        posx += self.button_width + padding_button
        self.stop_button = Button(master=self.controls_frame, command=self.stop, background=self.button_fg, foreground=self.controls_bg, activebackground=self.button_fg, activeforeground=self.controls_bg, image=self.img_button_stop, border='0', borderwidth=0, highlightthickness=0, relief=FLAT, width=self.button_width, height=self.button_height)
        self.stop_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')

        posx += self.button_width + padding_button
        self.record_button = Button(master=self.controls_frame, command=self.record, background=self.button_fg, foreground=self.controls_bg, activebackground=self.button_fg, activeforeground=self.controls_bg, image=self.img_button_record, border='0', borderwidth=0, highlightthickness=0, relief=FLAT, width=self.button_width, height=self.button_height)
        self.record_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')

        # Setup Meter Frame
        self.meter_frame = Frame(master, bg=self.meters_bg, width=self.window_width, height=self.meters_height)
        self.meter_frame.place(relx=0, rely=0, anchor='nw', x=0, y=self.controls_height)

        # Setup Input/Output Frames (split meter frame into 2)
        self.input_frame = Frame(master=self.meter_frame, bg=self.meters_bg, width=self.meters_inputs_width, height=self.meters_height)
        self.input_frame.place(relx=0, rely=0, anchor='nw', x=0, y=0)

        self.output_frame = Frame(master=self.meter_frame, bg=self.meters_bg, width=self.meters_outputs_width, height=self.meters_height)
        self.output_frame.place(relx=0, rely=0, anchor='nw', x=self.meters_inputs_width, y=0)

        # Setup Labels for Meter Frame
        self.inputs_label = Label(master=self.input_frame, text='INPUT', fg=self.label_fg, bg=self.meters_bg, font=(self.label_font_family, self.label_font_size))
        self.inputs_label.place(anchor='center', x=self.meters_inputs_width / 2, y=self.meter_label / 2)

        self.outputs_label = Label(master=self.output_frame, text='OUTPUT', fg=self.label_fg, bg=self.meters_bg, font=(self.label_font_family, self.label_font_size))
        self.outputs_label.place(anchor='center', x=self.meters_outputs_width / 2, y=self.meter_label / 2)

        # Create Input Meters
        self.input_meters = []
        padding_input_meter_x = (self.meters_inputs_width - self.meter_width * self.audio_channels_in) / (self.audio_channels_in + 1);
        padding_input_meter_y = (self.meters_height - self.meter_label - self.meter_sublabel - self.meter_height) / 2

        posx = padding_input_meter_x
        posy = padding_input_meter_y + self.meter_label
        for i in range(0, self.audio_channels_in):
            self.input_meters.append(Meter(master=self.input_frame, width=self.meter_width, height=self.meter_height, bg=self.window_bg, bd=0, highlightthickness=1, highlightbackground=self.meter_color, relief=FLAT))

            self.input_meters[i].place(relx=0, rely=0, anchor='nw', x=posx, y=posy)

            self.input_meters[i].set_color(self.meter_color)
            self.input_meters[i].set_avg_level(float(i) / float(self.audio_channels_in - 1))
            self.input_meters[i].set_max_level((float(i) + 0.5) / float(self.audio_channels_in - 1))

            self.input_meters[i].draw()

            input_label = Label(master=self.input_frame, text=str(i + 1), fg=self.label_fg, bg=self.meters_bg, font=(self.label_font_family, self.label_font_size_small))
            input_label.place(anchor='center', x=posx + self.meter_width / 2, y=posy + self.meter_height + padding_input_meter_y + self.meter_sublabel / 2)

            posx += padding_input_meter_x + self.meter_width

        # Create Output Meters
        self.output_meters = []
        padding_output_meter_x = (self.meters_outputs_width - self.meter_width * self.audio_channels_out) / (self.audio_channels_out + 1);
        padding_output_meter_y = (self.meters_height - self.meter_label - self.meter_sublabel - self.meter_height) / 2

        posx = padding_output_meter_x
        posy = padding_output_meter_y + self.meter_label
        for i in range(0, self.audio_channels_out):
            self.output_meters.append(Meter(master=self.output_frame, width=self.meter_width, height=self.meter_height, bg=self.window_bg, bd=0, highlightthickness=1, highlightbackground=self.meter_color, relief=FLAT))

            self.output_meters[i].place(relx=0, rely=0, anchor='nw', x=posx, y=posy)

            self.output_meters[i].set_color(self.meter_color)
            self.output_meters[i].set_avg_level(float(i) / float(self.audio_channels_out - 1))
            self.output_meters[i].set_max_level((float(i) + 0.5) / float(self.audio_channels_out - 1))

            self.output_meters[i].draw()

            output_label = Label(master=self.output_frame, text=str(i + 1), fg=self.label_fg, bg=self.meters_bg, font=(self.label_font_family, self.label_font_size_small))
            output_label.place(anchor='center', x=posx + self.meter_width / 2, y=posy + self.meter_height + padding_output_meter_y + self.meter_sublabel / 2)

            posx += padding_output_meter_x + self.meter_width

        # Initialize Audio
        self.audio = PiFieldRecorderAudio(self, 1, 15, 48000, 256)
        self.audio.start()

    def record(self):
        print('Record')

    def pause(self):
        print('Pause')

    def stop(self):
        print('Stop')

    def play(self):
        print('Play')

    def audio_update(self, audio, avg_levels, max_levels):
        for i in range(0, min(self.audio_channels_in, len(avg_levels['input']))):
            self.input_meters[i].set_avg_level(avg_levels['input'][i])
            self.input_meters[i].set_max_level(max_levels['input'][i])
            self.input_meters[i].clear()
            self.input_meters[i].draw()

        for i in range(0, min(self.audio_channels_out, len(avg_levels['output']))):
            self.output_meters[i].set_avg_level(avg_levels['output'][i])
            self.output_meters[i].set_max_level(max_levels['output'][i])
            self.output_meters[i].clear()
            self.output_meters[i].draw()

    def _destroy(self, event):
        self.master.unbind('<Destroy>')

        # Deinitialize Audio
        self.audio.destroy()

class Meter(Canvas):
    def __init__(self, **kwargs):
        Canvas.__init__(self, **kwargs)
        self.bind('<Configure>', self.redraw)

        self._color = '#ffffff'
        self._avg_level = 0.0
        self._max_level = 0.0

        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def set_color(self, color='#ffffff'):
        self._color = color

    def set_avg_level(self, level=0):
        if level < 0.0:
            level = 0.0
        if level > 1.0:
            level = 1.0
        self._avg_level = level

    def set_max_level(self, level=0):
        if level < 0.0:
            level = 0.0
        if level > 1.0:
            level = 1.0
        self._max_level = level

    def redraw(self, event):
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.clear()
        self.draw()

    def clear(self):
        # Delete all existing items
        self.delete(ALL)

    def draw(self):
        # Draw Average Level
        avg_pos = int(self.height * (1 - self._avg_level))
        self.create_rectangle(0, self.height, self.width, avg_pos, fill=self._color)

        # Draw Max Level
        max_pos = int(self.height * (1 - self._max_level))
        self.create_rectangle(0, max_pos, self.width, max_pos + 3, fill=self._color)

def main():
    root = Tk()
    app = PiFieldRecorderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
