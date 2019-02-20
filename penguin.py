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
isCombat, combat_mode = True, None
signal_level, signal = 3, None
orig_mouse_pointer = None
attack_mode = False
current_orientation = 0
can_rotate = True


toggle_delay = 250

white = (255, 255, 255)

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

def orient_left ():
    global current_orientation
    can_rotate = True
    if current_orientation == 0 and can_rotate == True:
		orient270 ()
		print ("rotated to 270 left")
		can_rotate = False
		current_orientation = 270
    elif current_orientation == 270 and can_rotate == True:
		orient180 ()
		print ("rotated to 180 left")
		can_rotate = False
		current_orientation = 180
    elif current_orientation == 180 and can_rotate == True:
		orient90 ()
		print ("rotated to 90 left")
		can_rotate = False
		current_orientation = 90
    elif current_orientation == 90 and can_rotate == True:
		orient0 ()
		print ("rotated to 0 left")
		can_rotate = False
		current_orientation = 0

def orient_right ():
    global current_orientation
    can_rotate = True
    if current_orientation == 0 and can_rotate == True:
		orient90 ()
		print ("rotated to 90 right")
		can_rotate = False
		current_orientation = 90
    elif current_orientation == 90 and can_rotate == True:
		orient180 ()
		print ("rotated to 180 right")
		can_rotate = False
		current_orientation = 180
    elif current_orientation == 180 and can_rotate == True:
		orient270 ()
		print ("rotated to 270 right")
		can_rotate = False
		current_orientation = 270
    elif current_orientation == 270 and can_rotate == True:
        orient0 ()
        print ("rotated to 0 right")
        can_rotate = False
        current_orientation = 0

def orient_back ():
    global current_orientation, can_rotate
    can_rotate = True
    global current_orientation
    if current_orientation == 0 and can_rotate == True:
		orient180 ()
		print ("rotated to 180")
		can_rotate = False
		current_orientation = 180
    if current_orientation == 90 and can_rotate == True:
		orient270 ()
		print ("rotated to 270")
		can_rotate = False
		current_orientation = 270
    if current_orientation == 180 and can_rotate == 1:
		orient0 ()
		print ("rotated to 0")
		can_rotate = False
		current_orientation = 0
    if current_orientation == 270 and can_rotate == 1:
        orient90 ()
        print ("rotated to 90")
        can_rotate = False
        current_orientation = 90


def image_list (name):
    return [touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)).white2grey (.5),
            touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)).white2grey (.1),
            touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)),
            touchgui.image_gui ("images/PNG/White/2x/%s.png" % (name)).white2rgb (.1, .2, .4)]

def combat_list (name):
    return [touchgui.image_gui ("images/%s.png" % (name)).white2grey (.5),
            touchgui.image_gui ("images/%s.png" % (name)).white2grey (.1),
            touchgui.image_gui ("images/%s.png" % (name)),
            touchgui.image_gui ("images/%s.png" % (name)).white2rgb (.1, .2, .4)]



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
    
def test_ping ():
    print ("I'm a button that works when clicked!")


def main ():
    global tabletOrMouse, audio, orig_mouse_pointer, combat_mode, white

    pygame.init ()
    pygame.font.init()
    textfont = pygame.font.SysFont("monospace", 15)
    if full_screen:
        #gameDisplay = pygame.display.set_mode ((display_width, display_height), FULLSCREEN)
		gameDisplay = pygame.display.set_mode ((display_width, display_height))
    else:
        gameDisplay = pygame.display.set_mode ((display_width, display_height))

    orig_mouse_pointer = pygame.mouse.get_cursor ()

    pygame.display.set_caption ("Penguin Tower")
    touchgui.set_display (gameDisplay, display_width, display_height)
    isoobject.set_display (gameDisplay, display_width, display_height)

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

    combat_mode = [touchgui.form ([touchgui.image_tile(combat_list ("bombresize"), touchgui.posX (0.95), touchgui.posY (0.1), 100, 100, test_ping),
                                   touchgui.image_tile(combat_list ("arrowresize"), touchgui.posX (0.95), touchgui.posY (0.3), 100, 100, test_ping),
                                   touchgui.image_tile(combat_list ("slashresize"), touchgui.posX (0.95), touchgui.posY (0.5), 100, 100, test_ping),
                                   touchgui.image_tile(image_list ("cross"), touchgui.posX (0.95), touchgui.posY (0.7), 100, 100, test_ping)]
)]

    controls = [touchgui.form ([touchgui.image_tile (image_list ("power"), #Power Button, to shut the app down. OR perhaps just use the tablet's OS to shut the app down?
                                                     touchgui.posX (0.95), touchgui.posY (1.0),
                                                     100, 100, myquit),

                                audio,

                                touchgui.image_tile (image_list ("singleplayer"),   #Supposedly disconnects/connects the player to a server?
                                                     touchgui.posX (0.05), touchgui.posY (1.0),
                                                     100, 100, orient270),

                                tabletOrMouse, signal,

    ])]

    movement_arrows = [touchgui.form ([touchgui.image_tile (image_list ("arrowUp"),
                                                     touchgui.posX (0.05), touchgui.posY (0.30),
                                                     100, 100),

                                touchgui.image_tile (image_list ("arrowLeft"),
                                                     touchgui.posX (0.00), touchgui.posY (0.20),
                                                     100, 100, orient_left),

                                touchgui.image_tile (image_list ("arrowRight"),
                                                     touchgui.posX (0.10), touchgui.posY (0.20),
                                                     100, 100, orient_right),

                                touchgui.image_tile (image_list ("arrowDown"),
                                                     touchgui.posX (0.05), touchgui.posY (0.10),
                                                     100, 100, orient_back),

                                touchgui.image_tile (image_list ("singleplayer"),   #Supposedly disconnects/connects the player to a server?
                                                     touchgui.posX (0.05), touchgui.posY (1.0),
                                                     100, 100, orient270),

    ])]
    
    label = textfont.render("TEST", 1 , white)

    forms = controls + movement_arrows + combat_mode
    isoobject.testRoom ()                  #Renders a basic 3D room for us
    touchgui.select (forms, myquit)


main ()
