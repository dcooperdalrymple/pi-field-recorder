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
    meters_outpus_width = 180

    # Labels
    label_fg = (0, 164, 0)
    label_font_family = 'Monospace'
    label_font_size = 12
    label_font_size_small = 8
    label_font_size_large = 16

    # Buttons
    button_width = 64
    button_height = 64
    button_fg = (0, 164, 0)
    button_active_fg = (0, 228, 0)

    # Meters
    meter_label = 18
    meter_sublabel = 16
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

        # Setup Labels for Meter Frame

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

        self.screen.blit(self.background, (0, 0))
        self.buttons.draw(self.screen)
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

    def update_levels(self, levels, max_levels):
        return

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
