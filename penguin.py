#!/usr/bin/env python

import pygame, touchgui, palate, isoobject
from pygame.locals import *

# display_width, display_height = 1920, 1080
display_width, display_height = 800, 600
display_width, display_height = 1920, 1080
full_screen = False
full_screen = True
isTablet, tabletOrMouse = False, None
isAudio, audio = True, None
signal_level, signal = 3, None
orig_mouse_pointer = None

toggle_delay = 250


def myquit ():
    pygame.display.update ()
    pygame.time.delay (toggle_delay * 2)
    pygame.quit ()
    quit ()

def orient0 ():
    isoobject.screen_orientation (0)

def orient90 ():
    isoobject.screen_orientation (90)

def orient180 ():
    isoobject.screen_orientation (180)

def orient270 ():
    isoobject.screen_orientation (270)

def image_list (name):
    return [touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)).white2grey (.5),
            touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)).white2grey (.1),
            touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)),
            touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)).white2rgb (.1, .2, .4)]

def flipAudio ():
    global isAudio, audio

    pygame.display.update ()
    pygame.time.delay (toggle_delay)
    if isAudio:
        isAudio = False
        audio.set_images (image_list ("audioOff"))
    else:
        isAudio = True
        audio.set_images (image_list ("audioOn"))

def flipMouseTablet ():
    global isTablet, tabletOrMouse

    pygame.display.update ()
    pygame.time.delay (toggle_delay)
    if isTablet:
        isTablet = False
        tabletOrMouse.set_images (image_list ("mouse"))
        pygame.mouse.set_cursor (*orig_mouse_pointer)  # extract list contents and pass as parameters
    else:
        isTablet = True
        # generate an invisible mouse pointer
        pygame.mouse.set_cursor ((8,8), (0,0), (0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))
        tabletOrMouse.set_images (image_list ("tablet"))


def signal_value (n):
    global signal_level, signal
    signal_level = n
    signal.set_images (image_list ("signal%d" % (n)))


def main ():
    global tabletOrMouse, audio, orig_mouse_pointer

    pygame.init ()
    if full_screen:
        #gameDisplay = pygame.display.set_mode ((display_width, display_height), FULLSCREEN)
		gameDisplay = pygame.display.set_mode ((display_width, display_height))
    else:
        gameDisplay = pygame.display.set_mode ((display_width, display_height))

    orig_mouse_pointer = pygame.mouse.get_cursor ()

    pygame.display.set_caption ("Penguin Tower")
    touchgui.set_display (gameDisplay, display_width, display_height)
    isoobject.set_display (gameDisplay, display_width, display_height)
    key_pad = [touchgui.form ([touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,       #Numbers placed on the bottom right of the screen. Perhaps merge into a single movement?
                                                   "1", touchgui.unitY (0.05),                               #Calls text_tile. Seems to create a simple box with text.
                                                   touchgui.posX (0), touchgui.posY (0.05),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "2", touchgui.unitY (0.05),
                                                   touchgui.posX (0.05), touchgui.posY (0.05),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "3", touchgui.unitY (0.05),
                                                   touchgui.posX (0.1), touchgui.posY (0.05),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "4", touchgui.unitY (0.05),
                                                   touchgui.posX (0), touchgui.posY (0.1),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "5", touchgui.unitY (0.05),
                                                   touchgui.posX (0.05), touchgui.posY (0.1),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "6", touchgui.unitY (0.05),
                                                   touchgui.posX (0.1), touchgui.posY (0.1),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "7", touchgui.unitY (0.05),
                                                   touchgui.posX (0), touchgui.posY (0.15),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "8", touchgui.unitY (0.05),
                                                   touchgui.posX (0.05), touchgui.posY (0.15),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
                               touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                                   "9", touchgui.unitY (0.05),
                                                   touchgui.posX (0.1), touchgui.posY (0.15),
                                                   touchgui.unitX (0.045), touchgui.unitY (0.045)),
    ])]

    tabletOrMouse = touchgui.image_tile (image_list ("tablet"),                     #As far as i'm aware, this hides the mouse. Probably expects a touch input to be equivalent to a mouse click
                                         touchgui.posX (0.1), touchgui.posY (1.0),  #Calls image_tile. Seems to create a "blank" box with an image. Needs to be transparent otherwise we get a background?
                                         100, 100, flipMouseTablet)

    audio = touchgui.image_tile (image_list ("audioOn"),                            #Determine whether Audio will be played or not
                                 touchgui.posX (0.0), touchgui.posY (1.0),
                                 100, 100, flipAudio)

    signal = touchgui.image_tile (image_list ("signal1"),                           #Perhaps showcases Wi-Fi signal strength.
                                  touchgui.posX (0.15), touchgui.posY (1.0),
                                  100, 100, orient270)

    """
    divide = touchgui.text_tile (palate.red, palate.green, palate.blue, palate.gold,
                                 u'\u00F7', touchgui.unitY (0.05),
                                 touchgui.posX (0.15), touchgui.posY (1.0),
                                 100, 100, orient270)
    """

    controls = [touchgui.form ([touchgui.image_tile (image_list ("power"),          #Power Button, to shut the app down. OR perhaps just use the tablet's OS to shut the app down?
                                                     touchgui.posX (0.95), touchgui.posY (1.0),
                                                     100, 100, myquit),

                                touchgui.image_tile (image_list ("upLeft"),         #orients the screen around. Perhaps merge them for a single rotate depending on current direction?
                                                     touchgui.posX (0.90), touchgui.posY (0.20),
                                                     100, 100, orient0),

                                touchgui.image_tile (image_list ("upRight"),
                                                     touchgui.posX (0.95), touchgui.posY (0.20),
                                                     100, 100, orient90),

                                touchgui.image_tile (image_list ("downLeft"),
                                                     touchgui.posX (0.90), touchgui.posY (0.10),
                                                     100, 100, orient180),

                                touchgui.image_tile (image_list ("downRight"),
                                                     touchgui.posX (0.95), touchgui.posY (0.10),
                                                     100, 100, orient270),

                                audio,

                                touchgui.image_tile (image_list ("singleplayer"),   #Supposedly disconnects/connects the player to a server?
                                                     touchgui.posX (0.05), touchgui.posY (1.0),
                                                     100, 100, orient270),

                                tabletOrMouse, signal,

    ])]

    forms = key_pad + controls
    isoobject.testRoom ()                  #Renders a basic 3D room for us
    touchgui.select (forms, myquit)


main ()
