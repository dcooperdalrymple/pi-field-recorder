# Pi Field Recorder: Battery-operated field recorder designed for use with the Audio Injector Octo and piTFT touch screen.

from app.controller import AppController

from app.viewurwid import AppViewUrwid # Terminal UI
from app.viewtkinter import AppViewTkinter # Window UI
#from app.viewpygame import AppViewPygame # SDL UI

view = AppViewUrwid

def main():
    AppController(view).run()

if __name__ == '__main__':
    main()
