import os, sys
import pygame
from pygame.locals import *

if !pygame.font: print 'Warning: Fonts disabled'
#if !pygame.mixer: print 'Warning: Sound disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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

class PygameButton(pygame.sprite.Sprite):
    def __init__(self):
        return
