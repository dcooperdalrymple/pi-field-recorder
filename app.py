#!/usr/bin/env python

# Pi Field Recorder: Battery-operated field recorder designed for use with the Audio Injector Octo and piTFT touch screen.

from Tkinter import *
import Tkinter

from audio import PiFieldRecorderAudio

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
        self.img_button_play_disabled = PhotoImage(file="./assets/button-play-inactive.gif")
        self.img_button_pause = PhotoImage(file="./assets/button-pause.gif")
        self.img_button_pause_active = PhotoImage(file="./assets/button-pause-active.gif")
        self.img_button_pause_disabled = PhotoImage(file="./assets/button-pause-inactive.gif")
        self.img_button_stop = PhotoImage(file="./assets/button-stop.gif")
        self.img_button_stop_active = PhotoImage(file="./assets/button-stop-active.gif")
        self.img_button_stop_disabled = PhotoImage(file="./assets/button-stop-inactive.gif")
        self.img_button_record = PhotoImage(file="./assets/button-record.gif")
        self.img_button_record_active = PhotoImage(file="./assets/button-record-active.gif")
        self.img_button_record_disabled = PhotoImage(file="./assets/button-record-inactive.gif")

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

        self.play_button = ImageButton(master=self.controls_frame, width=self.button_width, height=self.button_height, bg=self.controls_bg, bd=0, highlightthickness=0, highlightbackground=self.controls_bg, relief=FLAT)
        self.play_button.set_image(self.img_button_play, 'normal')
        self.play_button.set_image(self.img_button_play_active, 'active')
        self.play_button.set_image(self.img_button_play_disabled, 'disabled')
        self.play_button.set_state('normal')
        self.play_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')
        self.play_button.bind('<Button-1>', self.play)

        posx += self.button_width + padding_button

        self.pause_button = ImageButton(master=self.controls_frame, width=self.button_width, height=self.button_height, bg=self.controls_bg, bd=0, highlightthickness=0, highlightbackground=self.controls_bg, relief=FLAT)
        self.pause_button.set_image(self.img_button_pause, 'normal')
        self.pause_button.set_image(self.img_button_pause_active, 'active')
        self.pause_button.set_image(self.img_button_pause_disabled, 'disabled')
        self.pause_button.set_state('normal')
        self.pause_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')
        self.pause_button.bind('<Button-1>', self.pause)

        posx += self.button_width + padding_button

        self.stop_button = ImageButton(master=self.controls_frame, width=self.button_width, height=self.button_height, bg=self.controls_bg, bd=0, highlightthickness=0, highlightbackground=self.controls_bg, relief=FLAT)
        self.stop_button.set_image(self.img_button_stop, 'normal')
        self.stop_button.set_image(self.img_button_stop_active, 'active')
        self.stop_button.set_image(self.img_button_stop_disabled, 'disabled')
        self.stop_button.set_state('normal')
        self.stop_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')
        self.stop_button.bind('<Button-1>', self.stop)

        posx += self.button_width + padding_button

        self.record_button = ImageButton(master=self.controls_frame, width=self.button_width, height=self.button_height, bg=self.controls_bg, bd=0, highlightthickness=0, highlightbackground=self.controls_bg, relief=FLAT)
        self.record_button.set_image(self.img_button_record, 'normal')
        self.record_button.set_image(self.img_button_record_active, 'active')
        self.record_button.set_image(self.img_button_record_disabled, 'disabled')
        self.record_button.set_state('normal')
        self.record_button.place(relx=0, rely=0, x=posx, y=posy, anchor='nw')
        self.record_button.bind('<Button-1>', self.record)

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

    # Button Events

    def play(self, event):
        if self.play_button.get_state() == 'disabled':
            return
        self.audio.play()

    def pause(self, event):
        if self.pause_button.get_state() == 'disabled':
            return
        self.audio.pause()

    def stop(self, event):
        if self.stop_button.get_state() == 'disabled':
            return
        self.audio.stop()

    def record(self, event):
        if self.record_button.get_state() == 'disabled':
            return
        self.audio.record()

    # Audio Updates

    def state_update(self, state):
        print(state)
        if state == 'play':
            self.play_button.set_state('active')
            self.pause_button.set_state('normal')
            self.stop_button.set_state('normal')
            self.record_button.set_state('disabled')
        elif state == 'play_pause':
            self.play_button.set_state('active')
            self.pause_button.set_state('active')
            self.stop_button.set_state('normal')
            self.record_button.set_state('disabled')
        elif state == 'record':
            self.play_button.set_state('disabled')
            self.pause_button.set_state('normal')
            self.stop_button.set_state('normal')
            self.record_button.set_state('active')
        elif state == 'record_pause':
            self.play_button.set_state('disabled')
            self.pause_button.set_state('active')
            self.stop_button.set_state('normal')
            self.record_button.set_state('active')
        elif state == 'none':
            self.play_button.set_state('normal')
            self.pause_button.set_state('disabled')
            self.stop_button.set_state('disabled')
            self.record_button.set_state('normal')

    def audio_update(self, audio, avg_levels, max_levels):
        for i in range(0, min(self.audio_channels_in, len(avg_levels['input']))):
            self.input_meters[i].set_avg_level(avg_levels['input'][i])
            self.input_meters[i].set_max_level(max_levels['input'][i])
            self.input_meters[i].draw()

        for i in range(0, min(self.audio_channels_out, len(avg_levels['output']))):
            self.output_meters[i].set_avg_level(avg_levels['output'][i])
            self.output_meters[i].set_max_level(max_levels['output'][i])
            self.output_meters[i].draw()

    def _destroy(self, event):
        self.master.unbind('<Destroy>')

        # Deinitialize Audio
        self.audio.destroy()

class ImageButton(Canvas):
    def __init__(self, **kwargs):
        Canvas.__init__(self, **kwargs)

        self._state = False

        self._image_normal = False
        self._image_active = False
        self._image_disabled = False

        self._image_id = False

        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def set_state(self, state='normal'):
        if self._state == state:
            return
        self._state = state
        self.draw()

    def get_state(self):
        return self._state

    def set_image(self, image, state):
        if state == 'normal':
            self._image_normal = image
        elif state == 'active':
            self._image_active = image
        elif state == 'disabled':
            self._image_disabled = image

    def draw(self):
        self._clear()
        self._draw()

    def _clear(self):
        if self._image_id != None and self._image_id != False:
            self.delete(self._image_id)
            self._image_id = False

    def _draw(self):
        image = False
        if self._state == 'normal' and self._image_normal != False:
            image = self._image_normal
        elif self._state == 'active' and self._image_active != False:
            image = self._image_active
        elif self._state == 'disabled' and self._image_disabled != False:
            image = self._image_disabled

        if image == False:
            return False

        try:

            # Draw Image
            self._image_id = self.create_image((self.width / 2, self.height / 2), image=image, state=NORMAL, anchor=CENTER)

        except:
            print('Failed to render ImageButton')
            return False

        return True

class Meter(Canvas):
    def __init__(self, **kwargs):
        Canvas.__init__(self, **kwargs)

        self._color = '#ffffff'
        self._avg_level = 0.0
        self._max_level = 0.0

        self._avg_rectangle_id = False
        self._max_rectangle_id = False

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

    def draw(self):
        self._clear()
        self._draw()

    def _clear(self):
        # Delete all existing items
        if self._avg_rectangle_id != None and self._avg_rectangle_id != False:
            self.delete(self._avg_rectangle_id)
            self._avg_rectangle_id = False
        if self._max_rectangle_id != None and self._max_rectangle_id != False:
            self.delete(self._max_rectangle_id)
            self._max_rectangle_id = False

    def _draw(self):
        try:

            # Draw Average Level
            avg_pos = int(self.height * (1 - self._avg_level))
            self._avg_rectangle_id = self.create_rectangle(0, self.height, self.width, avg_pos, fill=self._color)

            # Draw Max Level
            max_pos = int(self.height * (1 - self._max_level))
            self._max_rectangle_id = self.create_rectangle(0, max_pos, self.width, max_pos + 3, fill=self._color)

        except:
            print('Failed to render Meter')
            return False

        return True

def main():
    root = Tk()
    app = PiFieldRecorderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
