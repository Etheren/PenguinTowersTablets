#!/usr/bin/env python

debugging = False
debugging = True
isActivating = False

import pygame, os
from pygame.locals import *


from palate import *

display_width, display_height = None, None
fuzz = "100%"


#
#  set_resolution - configures the resolution for the gui display.
#                   This must be called before, select.
#

def set_resolution (x, y):
    global display_width, display_height
    display_width, display, height = x, y


#
#  unitX - v is a floating point number and unitX returns the
#          distance in pixels.  0.0..1.0  X axis.
#

def unitX (v):
    return int (v * display_width)

#
#  unitY - v is a floating point number and unitY returns the
#          distance in pixels.  0.0..1.0  Y axis.
#

def unitY (v):
    return int (v * display_height)

#
#  posX - v is a floating point number and posX returns the
#         position in pixels.  0.0..1.0  X axis.
#

def posX (v):
    return int (v * display_width)

#
#  posY - v is a floating point number and posY returns the
#         position in pixels.  0.0..1.0  X axis.
#

def posY (v):
    return display_height - unitY (v)

class form:
    def __init__ (self, children):
        self.active = False
        self.frozen = False
        self.children = children
    def set_active (self, b):
        for c in self.children:
            c.set_active (b)
        self.active = b
    def set_frozen (self, b):
        for c in self.children:
            c.set_frozen (b)
        self.frozen = b
    def update (self):
        for c in self.children:
            c.update ()
    def select (self):
        for c in self.children:
            c.select ()
    def deselect (self):
        for c in self.children:
            c.deselect ()

def text_objects (text, font, colour = white):
    textSurface = font.render (text, True, colour)
    return textSurface, textSurface.get_rect ()

# tile_state enumerated type.  Order must be coordinated with the _colours list below
tile_frozen, tile_active, tile_activated, tile_pressed = range (4)

class text_tile:
    def __init__ (self, default_colour, activated_colour, pressed_colour, frozen_colour,    #Draws a text box, and needs the following params :
                  text_message, text_size,                                                  #The standard colour of the box, the "activated" colour, the colour when the button is pressed, the "frozen" colour
                  x, y, width, height, action=None, flush=None):                            #The text in the box (Must be in between "X"), Size of the text 0-1, the location of the box on the screen (what point does this relate to?)
        # the _colour list must be in this order (the same as the tile_state above)         #The size of the box, what the button does when pressed (defaulted to nothing), "flush" (defaults to nothing)
        self._colours = [frozen_colour, default_colour, activated_colour, pressed_colour]
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._action = action
        self._text_message = text_message
        self._text_size = text_size
        self._text_font = pygame.font.SysFont (None, text_size)
        self._text_surf, self._text_rect = text_objects (text_message, self._text_font, white)
        self._text_rect.center = ( (x+(width/2)), (y+(height/2)) )
        self._state = tile_active
        self._flush = flush
    #
    #  select - test to see if the mouse position is over the tile and it is not frozen
    #           and if the mouse is activated call the action.
    #  Look at Image_Tile.select to understand stuff about this function.
    #
    def select (self):
        global isActivating
        if self._state != tile_frozen:
            mouse = pygame.mouse.get_pos ()
            click = pygame.mouse.get_pressed ()
            if self._x+self._width > mouse[0] > self._x and self._y+self._height > mouse[1] > self._y:
                self.set_activated ()
                if click[0] == 1:
                    self.set_pressed ()
                    if self._action != None and isActivating == False:
                        self._action ()
                        isActivating = True

    def deselect (self):
        if self._state != tile_frozen:
            self.set_active ()
    #
    #  set_active - change the tile state to active and update if necessary
    #
    def set_active (self):
        if self._state != tile_active:
            self._state = tile_active
            self.update ()
    #
    #  set_activated - change the tile state to activated and update if necessary
    #
    def set_activated (self):
        if self._state != tile_activated:
            self._state = tile_activated
            self.update ()
    #
    #  set_frozen - change the tile state to frozen and update if necessary
    #
    def set_frozen (self):
        if self._state != tile_frozen:
            self._state = tile_frozen
            self.update ()
    #
    #  set_pressed - change the tile state to pressed and update if necessary
    #
    def set_pressed (self):
        if self._state != tile_frozen:
            self._state = tile_pressed
            self.update ()
    #
    #  update - redraw the tile.
    #
    def update (self):
        # print "update text_tile",
        pygame.draw.rect (gameDisplay, self._colours[self._state],
                          (self._x, self._y, self._width, self._height))
        # print self._x, self._y, self._width, self._height, self._y - self._height
        gameDisplay.blit (self._text_surf, self._text_rect)
        
    #
    # updateText - update the text that is on the text tile
    #

    def updateText (self, newText):
        self._text_message = newText
        self._text_surf, self._text_rect = text_objects (self._text_message, self._text_font, white)
        self._text_rect.center = ( (self._x+(self._width/2)), (self._y+(self._height/2)) )
        self.update()

    #
    # updateColours - update the 4 colours for the button
    #

    def updateColours(self, newFrozen, newActive, newActivated, newPressed):
        self._colours = [newFrozen, newActive, newActivated, newPressed]
        self.update()
    
    #
    #  flush_display - call the callback if one is registered.
    #
    def flush_display (self):
        if not (self._flush is None):
            self._flush ()

def load_image (name):
    return pygame.image.load (name).convert_alpha ()


def cache_file (name):
    return os.path.join (os.path.join (os.path.join (os.environ["HOME"], ".cache"), "touchgui"), name)

def cache_exists (name):
    return os.path.isfile (cache_file (name))

def allowActivation ():
    global isActivating
    isActivating = False

def _errorf (s):
    print s
    os.sys.exit (1)


class image_gui:
    def __init__ (self, name):
        if not os.path.isfile (name):
            _errorf ("image " + name + " not found")
        self.name = name

    #
    #  grey -
    #

    def grey (self):
        newname = "%s-grey" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        os.system ("convert %s -set colorspace Gray -separate -average %s" % (self.name, cache_file (newname)))
        self.name = newname
        return self

    #
    #  white2red -
    #

    def white2red (self):
        newname = "%s-red" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        os.system ("convert %s -fuzz %s -fill red -opaque white %s" % (self.name, fuzz, cache_file (newname)))
        self.name = newname
        return self

    #
    #  white2blue -
    #

    def white2blue (self):
        newname = "%s-blue" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        os.system ("convert %s -fuzz %s -fill blue -opaque white %s" % (self.name, fuzz, cache_file (newname)))
        self.name = newname
        return self

    #
    #  white2grey -
    #

    def white2grey (self, value=.85):
        newname = "%s-grey" % (self.name.split ("/")[-1])
        if cache_exists (newname):
            self.name = newname
            return self
        os.system ("convert %s -fuzz %s -fill 'rgb(%d,%d,%d)' -opaque white %s" % (self.name, fuzz,
                                                                                   int (value * 255.0), int (value * 255.0), int (value * 255.0),
                                                                                   cache_file (newname)))
        self.name = newname
        return self

    #
    #  white2rgb -
    #

    def white2rgb (self, r=.85, g=.85, b=.85):
        r = int (r * 256.0)
        g = int (g * 256.0)
        b = int (b * 256.0)
        newname = "%s-rgb-%d-%d-%d" % (self.name.split ("/")[-1], r, g, b)
        if cache_exists (newname):
            self.name = newname
            return self
        os.system ("convert %s -fuzz %s -fill 'rgb(%d,%d,%d)' -opaque white %s" % (self.name, fuzz, r, g, b, cache_file (newname)))
        self.name = newname
        return self

    #
    #  resize -
    #

    def resize (self, width, height):
        newname = "%s-%dx%d" % (self.name.split ("/")[-1], width, height)
        if cache_exists (newname):
            self.name = newname
            return newname
        os.system ("convert %s -resize %dx%d %s" % (self.name, width, height, cache_file (newname)))
        self.name = newname
        return self

    #
    #  load_image -
    #

    def load_image (self):
        if cache_exists (self.name):
            return pygame.image.load (cache_file (self.name)).convert_alpha ()
        return pygame.image.load (self.name).convert_alpha ()


class image_tile:
    def __init__ (self, image_list,                                                   #create an image button, needs an image list created in a file, location and size of the image, what happens when pressed, then "flush"
                  x, y, width, height, action=None, flush=None):                      #Similar to the text box, but requires a bit more input, especially needing to load an image into the program
        #  the _image list must be in this order (the same as the tile_state above)   #(Check image_list in penguin.py. uses image_gui constructor located in this file.)
        self._images = image_list
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._action = action
        self._state = tile_active
        self._flush = flush
    #
    #  select - test to see if the mouse position is over the tile and it is not frozen
    #           and if the mouse is activated call the action.
    def select (self):
        global isActivating
        if self._state != tile_frozen:
            mouse = pygame.mouse.get_pos ()
            click = pygame.mouse.get_pressed ()
            if self._x+self._width > mouse[0] > self._x and self._y+self._height > mouse[1] > self._y:
                self.set_activated ()
                if click[0] == 1 and self._x+self._width > mouse[0] > self._x and self._y+self._height > mouse[1] > self._y:
                    self.set_pressed ()
                    if self._action != None and isActivating == False:
                        self._action ()
                        isActivating = True
    #
    #  dselect - set active all unfrozen tiles.
    #
    def deselect (self):
        if self._state != tile_frozen:
            self.set_active ()
    #
    #  set_active - change the tile state to active and update if necessary
    #
    def set_active (self):
        if self._state != tile_active:
            self._state = tile_active
            self.update ()
    #
    #  set_activated - change the tile state to activated and update if necessary
    #
    def set_activated (self):
        if self._state != tile_activated:
            self._state = tile_activated
            self.update ()
    #
    #  set_frozen - change the tile state to frozen and update if necessary
    #
    def set_frozen (self):
        if self._state != tile_frozen:
            self._state = tile_frozen
            self.update ()
    #
    #  set_pressed - change the tile state to pressed and update if necessary
    #
    def set_pressed (self):
        if self._state != tile_frozen:
            self._state = tile_pressed
            self.update ()
    #
    #  update - redraw the tile.
    #
    def update (self):
        self._image_rect = self._images[self._state].load_image ().get_rect ()
        self._image_rect.center = ( (self._x+(self._width/2)), (self._y+(self._height/2)) )

        # print "update text_tile",
        pygame.draw.rect (gameDisplay, black,
                          (self._x, self._y, self._width, self._height))
        # print self._x, self._y, self._width, self._height, self._y - self._height
        gameDisplay.blit (self._images[self._state].load_image (), self._image_rect)
    #
    #  flush_display - call the callback if one is registered.
    #
    def flush_display (self):
        if not (self._flush is None):
            self._flush ()
    #
    #  set_images - set the image list to image_list.
    #
    def set_images (self, image_list):
        self._images = image_list
        self.update ()

def update (forms):
    for f in forms:
        f.update ()

def _select (forms):
    for f in forms:
        f.select ()

def deselect (forms):
    for f in forms:
        f.deselect ()


def select (forms, quit_func):
    global need_update, isActivating

    update (forms)
    pygame.display.update ()
    while True:
        event = pygame.event.wait ()
        if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
            quit_func ()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            _select (forms)
            update (forms)
            pygame.display.update ()
        elif event.type == pygame.MOUSEBUTTONUP:
            isActivating = False
            deselect (forms)
            _select (forms)
            update (forms)
            pygame.display.update ()
        else:
            _select (forms)
            update (forms)
            pygame.display.update ()
            deselect (forms)

def set_display (display, width, height):
    global gameDisplay, display_width, display_height
    gameDisplay = display
    display_width, display_height = width, height

def create_cache ():
    d = os.path.join (os.path.join (os.environ["HOME"], ".cache"), "touchgui")
    os.system ("mkdir -p %s" % (d))

def reset_cache ():
    d = os.path.join (os.path.join (os.environ["HOME"], ".cache"), "touchgui")
    os.system ("rm -r %s" % (d))

reset_cache ()
create_cache ()
