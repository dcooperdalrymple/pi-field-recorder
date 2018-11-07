#!/usr/bin/env python

import os, sys
import pygame
from pygame.locals import *
from app.view import AppView

class AppViewPygame(AppView):

    # Frames
    window_width = 320
    window_height = 240
    window_bg = (0, 0, 0)
    controls_height = 96
    meters_height = 144
    meters_inputs_width = 140
    meters_outputs_width = 180

    # Labels
    label_fg = (0, 164, 0)
    label_font_family = './assets/monospace.ttf'
    label_font_size = 24
    label_font_size_small = 18
    label_font_size_large = 36

    # Buttons
    button_width = 64
    button_height = 64
    button_fg = (0, 164, 0)
    button_active_fg = (0, 228, 0)

    # Meters
    meter_label = 28
    meter_sublabel = 20
    meter_height = 96
    meter_width = 16
    meter_border = 1
    meter_color = (0, 164, 0)

    def __init__(self, controller):
        AppView.__init__(self, controller)
        self._destroy = False

        if not pygame.font: print 'Warning: Fonts disabled'
        #if not pygame.mixer: print 'Warning: Sound disabled'

        # Initialize Pygame Window
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Pi Field Recorder')
        pygame.mouse.set_visible(1)

        # Setup Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.window_bg)

        # Display Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Configure and place buttons
        padding_button = (self.window_width - self.button_width * 4) / 5
        posy = (self.controls_height - self.button_height) / 2

        posx = padding_button

        self.play_button = PygameButton(normal_image="button-play.gif", active_image="button-play-active.gif", disabled_image="button-play-inactive.gif", pos=(posx, posy))

        posx += self.button_width + padding_button

        self.pause_button = PygameButton(normal_image="button-pause.gif", active_image="button-pause-active.gif", disabled_image="button-pause-inactive.gif", pos=(posx, posy))

        posx += self.button_width + padding_button

        self.stop_button = PygameButton(normal_image="button-stop.gif", active_image="button-stop-active.gif", disabled_image="button-stop-inactive.gif", pos=(posx, posy))

        posx += self.button_width + padding_button

        self.record_button = PygameButton(normal_image="button-record.gif", active_image="button-record-active.gif", disabled_image="button-record-inactive.gif", pos=(posx, posy))

        self.buttons = pygame.sprite.RenderPlain((self.play_button, self.pause_button, self.stop_button, self.record_button))

        # Setup Fonts
        if pygame.font:
            self.label_font = pygame.font.Font(self.label_font_family, self.label_font_size)
            self.label_font_small = pygame.font.Font(self.label_font_family, self.label_font_size_small)

        # Setup Labels for Meter Frame
        if pygame.font:
            # Inputs Label
            text = self.label_font.render('INPUT', 1, self.label_fg)
            textpos = text.get_rect(centerx=self.meters_inputs_width / 2, centery=self.controls_height + self.meter_label / 2)
            self.background.blit(text, textpos)

            # Outputs Label
            text = self.label_font.render('OUTPUT', 1, self.label_fg)
            textpos = text.get_rect(centerx=self.meters_inputs_width + self.meters_outputs_width / 2, centery=self.controls_height + self.meter_label / 2)
            self.background.blit(text, textpos)

        # Create Input Meters
        self.input_meters = []
        padding_input_meter_x = (self.meters_inputs_width - self.meter_width * self.controller.audio_channels_in) / (self.controller.audio_channels_in + 1)
        padding_input_meter_y = (self.meters_height - self.meter_label - self.meter_sublabel - self.meter_height) / 2

        posx = padding_input_meter_x
        posy = self.controls_height + padding_input_meter_y + self.meter_label

        for i in range(0, self.controller.audio_channels_in):
            self.input_meters.append(PygameMeter(pos=(posx, posy), size=(self.meter_width, self.meter_height)))

            self.input_meters[i].set_fore_color(self.meter_color)
            self.input_meters[i].set_avg_level(float(i) / float(self.controller.audio_channels_in - 1))
            self.input_meters[i].set_max_level((float(i) + 0.5) / float(self.controller.audio_channels_in - 1))

            self.input_meters[i].draw()

            # Draw sublabel
            if pygame.font:
                text = self.label_font_small.render(str(i + 1), 1, self.label_fg)
                textpos = text.get_rect(centerx=posx + self.meter_width / 2, centery=posy + self.meter_height + padding_input_meter_y + self.meter_sublabel / 2)
                self.background.blit(text, textpos)

            posx += padding_input_meter_x + self.meter_width

        # Create Output Meters
        self.output_meters = []
        padding_output_meter_x = (self.meters_outputs_width - self.meter_width * self.controller.audio_channels_out) / (self.controller.audio_channels_out + 1)
        padding_output_meter_y = (self.meters_height - self.meter_label - self.meter_sublabel - self.meter_height) / 2

        posx = self.meters_inputs_width + padding_output_meter_x
        posy = self.controls_height + padding_output_meter_y + self.meter_label

        for i in range(0, self.controller.audio_channels_out):
            self.output_meters.append(PygameMeter(pos=(posx, posy), size=(self.meter_width, self.meter_height)))

            self.output_meters[i].set_fore_color(self.meter_color)
            self.output_meters[i].set_avg_level(float(i) / float(self.controller.audio_channels_out - 1))
            self.output_meters[i].set_max_level((float(i) + 0.5) / float(self.controller.audio_channels_out - 1))

            self.output_meters[i].draw()

            # Draw sublabel
            if pygame.font:
                text = self.label_font_small.render(str(i + 1), 1, self.label_fg)
                textpos = text.get_rect(centerx=posx + self.meter_width / 2, centery=posy + self.meter_height + padding_output_meter_y + self.meter_sublabel / 2)
                self.background.blit(text, textpos)

            posx += padding_output_meter_x + self.meter_width

        self.meters = pygame.sprite.RenderPlain(tuple(self.input_meters + self.output_meters))

    def run(self):
        clock = pygame.time.Clock()
        while 1:
            self.update()

            if self._destroy == True:
                break

            clock.tick(60)

    def destroy(self):
        self._destroy = True

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.controller.destroy()
                return
            elif event.type == MOUSEBUTTONUP:
                # Mouse Click Events
                pos = pygame.mouse.get_pos()
                if self.play_button.check(pos):
                    self.controller.play()
                elif self.pause_button.check(pos):
                    self.controller.pause()
                elif self.stop_button.check(pos):
                    self.controller.stop()
                elif self.record_button.check(pos):
                    self.controller.record()

        self.buttons.update()
        self.meters.update()

        self.screen.blit(self.background, (0, 0))
        self.buttons.draw(self.screen)
        self.meters.draw(self.screen)
        pygame.display.flip()

    def update_state(self, state):
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
        else:
            return False

        return True

    def update_levels(self, avg_levels, max_levels):
        for i in range(0, min(self.controller.audio_channels_in, len(avg_levels['input']))):
            self.input_meters[i].set_avg_level(avg_levels['input'][i])
            self.input_meters[i].set_max_level(max_levels['input'][i])
            self.input_meters[i].draw()

        for i in range(0, min(self.controller.audio_channels_out, len(avg_levels['output']))):
            self.output_meters[i].set_avg_level(avg_levels['output'][i])
            self.output_meters[i].set_max_level(max_levels['output'][i])
            self.output_meters[i].draw()

        return True

class PygameButton(pygame.sprite.Sprite):
    def __init__(self, normal_image, active_image, disabled_image, pos):
        pygame.sprite.Sprite.__init__(self)

        self._image_normal, self._image_normal_rect = self._load_image(normal_image, -1)
        self._image_active, self._image_active_rect = self._load_image(active_image, -1)
        self._image_disabled, self._image_disabled_rect = self._load_image(disabled_image, -1)

        self._state = False
        self.set_state()

        self._pos = pos

    def set_state(self, state='normal'):
        if (self._state == state):
            return
        self._state = state
        self.image, self.rect = self._get_image()

    def check(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        self.rect.topleft = self._pos

    def _get_image(self):
        if self._state == 'normal':
            return self._image_normal, self._image_normal_rect
        elif self._state == 'active':
            return self._image_active, self._image_active_rect
        elif self._state == 'disabled':
            return self._image_disabled, self._image_disabled_rect
        else:
            return False, False

    def _load_image(self, name, colorkey=None):
        fullname = os.path.join('./assets', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message

        image = image.convert()
        if colorkey != None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)

        return image, image.get_rect()

class PygameMeter(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)

        self._back_color = (0, 0, 0)
        self._fore_color = (255, 255, 255)
        self._border_thickness = 1
        self._max_thickness = 2
        self._avg_level = 0.0
        self._max_level = 0.0

        # Setup Drawing Surface
        self._surface = pygame.Surface(size)
        self._surface = self._surface.convert()

        # Setup Sprite Image from Surface
        self.image = self._surface
        self.rect = self._surface.get_rect()

        self._pos = pos

    def set_back_color(self, color=(0, 0, 0)):
        self._back_color = color

    def set_fore_color(self, color=(255, 255, 255)):
        self._fore_color = color

    def set_avg_level(self, level=0.0):
        if level < 0.0:
            level = 0.0
        if level > 1.0:
            level = 1.0
        self._avg_level = level

    def set_max_level(self, level=0.0):
        if level < 0.0:
            level = 0.0
        if level > 1.0:
            level = 1.0
        self._max_level = level

    def update(self):
        self.rect.topleft = self._pos

    def draw(self):
        size = self._surface.get_rect()

        try:

            # Clear and Draw Background
            pygame.draw.rect(self._surface, self._back_color, (0, 0, size.width, size.height))

            # Draw Average Level
            avg_pos = int(float(size.height) * self._avg_level)
            pygame.draw.rect(self._surface, self._fore_color, (0, size.height - avg_pos, size.width, avg_pos))

            # Draw Max Level
            max_pos = int(float(size.height) * (1.0 - self._max_level))
            if self._max_thickness < 1:
                pygame.draw.line(self._surface, self._fore_color, (0, max_pos), (size.width, max_pos), 1)
            else:
                pygame.draw.line(self._surface, self._fore_color, (0, max_pos), (size.width, max_pos), self._max_thickness)

            # Draw Border
            if self._border_thickness > 0:
                pygame.draw.rect(self._surface, self._fore_color, (0, 0, size.width, size.height), self._border_thickness)

        except:
            print('Failed to render PygameMeter')
            return False

        return True
