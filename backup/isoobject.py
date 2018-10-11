#!/usr/bin/env python

import sys, os, pygame, random
from pygame.locals import *


numberOfTilesInX = 20

root6 = 2.44948974278
root3 = 1.73205080757
root2 = 1.41421356237
cosroot6 = -0.76990572975

glyphs = []
images = {}

MaxX               = 1920
MaxY               = 1080
mapAreaX           = 1920
mapAreaY           = 1080
unitX              =  mapAreaX / numberOfTilesInX
unitY              =  unitX * 2 #

numberOfTilesInY   = mapAreaY / unitY

default_resolution = (MaxX, MaxY)
White              = (255, 255, 255)
Black              = (0, 0, 0)
fullscreen         = True
prefix             = ""
family             = {}


class coord:
    def __init__ (self):
        pass

def is_odd (x):
    return (x % 2) == 1

def is_even (x):
    return (x % 2) == 0

def redraw_method (x, y):
    print x, y

def redraw (func):
    for row in range (numberOfTilesInY / 2):
        y = row
        func (y, y)
        if y > 0:
            y2 = y
            i = 0
            while i<y2:
                func (y2-(i+1), row)
                func (y2+(i+1), row)
                i += 1
    for row in range (numberOfTilesInY / 2):
        y = row + numberOfTilesInY / 2
        func (y, y)
        y2 = numberOfTilesInY / 2 - row
        i = 0
        while i<y2:
            func (y2-(i+1), y)
            func (y2+(i+1), y)
            i += 1
    func (numberOfTilesInY-1, numberOfTilesInY-1)

#
#  cart2iso - pre-condition:  x, y, z are cartesian coordinates.
#             post-condition:  x, y, z, are mapped into their isometric positions.
#

def cart2iso (x, y, z, xscale, yscale, xoffset, yoffset):
    """
    cx = 1.0/root6 * (root3 * x - root3 * z)
    cy = 1.0/root6 * (x + 2 * y + z)
    cz = 1.0/root6 * (root2 * x - root2 * y + root2 * z)
    return cx, cy, cz
    """
    cx = unitX * numberOfTilesInX / 2.0 + ((x - y) * xscale * unitX) / 2.0 + xoffset * unitX

    print "unitX =", unitX, "unitY =", unitY,
    print "numberOfTilesInX =", numberOfTilesInX, x, y,
    cx = unitX * numberOfTilesInX / 2.0 + ((x - y) * xscale * unitX) / 2.0 + xoffset * unitX
    cy = (x + y) * unitY * yscale + yoffset * unitY
    print "cx, cy =", cx, cy
    return cx, cy, 0


class glyph:
    def __init__ (self, x, y, z, xscale, yscale, xoffset, yoffset):
        self.cartesian = [x, y, z, xscale, yscale, xoffset, yoffset]
        self.isometric = cart2iso (x, y, z, xscale, yscale, xoffset, yoffset)
        self.image = None
    def set_image (self, image):
        self.image = image
        return self


#
#  isHorizontal - returns True if this line is horizontal.
#                 pre-condition: x0, y0, x1, y1 is either vertical or
#                 horizontal.
#                 post-condition: return y0 == y1.
#

def isHorizontal (x0, y0, x1, y1):
    return y0 == y1


#
#  isVertical - returns True if this line is vertical.
#               pre-condition: x0, y0, x1, y1 is either vertical or
#               horizontal.
#               post-condition: return x0 == x1.
#

def isVertical (x0, y0, x1, y1):
    return x0 == x1


#
#  fatal_error - issue an error and exit.
#

def fatal_error (format, *args):
    print str (format) % args,
    sys.exit (1)


def get_family (fullname):
    global family
    if family.has_key (fullname):
        return family[fullname]
    for lines in open ('DESC').readlines ():
        decomment = lines.split ('#')
        if (len (decomment) > 0) and (len (decomment[0]) > 0):
            if decomment[0][0].isalpha ():
                words = decomment[0].split ()
                name = words[0]
                value = []
                i = 1
                while (i < len (words)) and (len (value) <= 3):
                    value += [float (words[i])]
                    i += 1
                family[name] = value
    if family.has_key (fullname):
        return family[fullname]
    else:
        fatal_error ('DESC: does not contain an entry for %s\n', fullname)


#
#  hline - draw a horizontal line of images.
#

def hline (x0, y0, x1, y1, basename, orientation):
    for x in range (min (x0, x1), max (x0, x1)+1):
        s = get_family (basename + orientation)
        t = glyph (x, y0, 0, s[0], s[1], s[2], s[3]).set_image (get_image (basename + orientation))
        insert_glyph (t)

#
#  vline - draw a vertical line of images.
#

def vline (x0, y0, x1, y1, basename, orientation):
    for y in range (min (y0, y1), max (y0, y1)+1):
        s = get_family (basename + orientation)
        t = glyph (x0, y, 0, s[0], s[1], s[2], s[3]).set_image (get_image (basename + orientation))
        insert_glyph (t)

#
#  line - draw a vertical or horizontal line of images.
#

def line (x0, y0, x1, y1, basename):
    if isHorizontal (x0, y0, x1, y1):
        hline (x0, y0, x1, y1, basename)
    elif isVertical (x0, y0, x1, y1):
        vline (x0, y0, x1, y1, basename)
    else:
        fatal_error ('unexpected %s: %d, %d, %d, %d\n', basename, x0, y0, x1, y1)


#
#
#

def wall_n (x0, y0, x1, y1):
    hline (x0, y0, x1, y1, "stoneWall", "_N")

def wall_s (x0, y0, x1, y1):
    hline (x0, y0, x1, y1, "stoneWall", "_S")

#
#
#

def wall_e (x0, y0, x1, y1):
    vline (x0, y0, x1, y1, "stoneWall", "_E")


def wall_w (x0, y0, x1, y1):
    vline (x0, y0, x1, y1, "stoneWall", "_W")


def aged_wall_n (x0, y0, x1, y1):
    hline (x0, y0, x1, y1, "stoneWallAged", "_N")

def aged_wall_s (x0, y0, x1, y1):
    hline (x0, y0, x1, y1, "stoneWallAged", "_S")

def aged_wall_e (x0, y0, x1, y1):
    vline (x0, y0, x1, y1, "stoneWallAged", "_E")

def aged_wall_w (x0, y0, x1, y1):
    vline (x0, y0, x1, y1, "stoneWallAged", "_W")


#
#  wall - creates a wall object in the scene.  The walls in penguin tower are
#         vertical or horizontal only.
#         pre-condition:
#

def wall (x0, y0, x1, y1):
    line (x0, y0, x1, y1, "stoneWall")

#
#  closed_door - creates a closed door object in the scene.  The doors
#                in penguin tower are vertical or horizontal only.
#

def closed_door (x0, y0, x1, y1):
    line (x0, y0, x1, y1, "door")


#
#  open_door - creates an open door object in the scene.  The doors
#              in penguin tower are vertical or horizontal only.
#

def open_door (x0, y0, x1, y1):
    line (x0, y0, x1, y1, "floor")


#
#  secret_door - creates a secret door object in the scene.  The doors
#                in penguin tower are vertical or horizontal only.
#

def secret_door (x0, y0, x1, y1):
    line (x0, y0, x1, y1, "wall")

def place_named_glyph (x, y, basename, orientation):
    s = get_family (basename + orientation)
    t = glyph (x, y, 0, s[0], s[1], s[2], s[3]).set_image (get_image (basename + orientation))
    insert_glyph (t)

def corner_n (x, y):
    place_named_glyph (x, y, "stoneWallCorner", "_N")

def corner_s (x, y):
    place_named_glyph (x, y, "stoneWallCorner", "_S")

def corner_e (x, y):
    place_named_glyph (x, y, "stoneWallCorner", "_E")

def corner_w (x, y):
    place_named_glyph (x, y, "stoneWallCorner", "_W")

def broken_wall_n (x, y):
    place_named_glyph (x, y, "stoneWallBroken", "_N")

def broken_wall_e (x, y):
    place_named_glyph (x, y, "stoneWallBroken", "_E")

def broken_wall_s (x, y):
    place_named_glyph (x, y, "stoneWallBroken", "_S")

def broken_wall_w (x, y):
    place_named_glyph (x, y, "stoneWallBroken", "_W")

def broken_wall_left_n (x, y):
    place_named_glyph (x, y, "stoneWallBrokenLeft", "_N")

def broken_wall_left_e (x, y):
    place_named_glyph (x, y, "stoneWallBrokenLeft", "_E")

def broken_wall_left_s (x, y):
    place_named_glyph (x, y, "stoneWallBrokenLeft", "_S")

def broken_wall_left_w (x, y):
    place_named_glyph (x, y, "stoneWallBrokenLeft", "_W")

def short_wall_n (x0, y0, x1, y1):
    hline (x0, y0, x1, y1, "stoneWallTop", "_N")

def short_wall_s (x0, y0, x1, y1):
    hline (x0, y0, x1, y1, "stoneWallTop", "_S")

def short_wall_e (x0, y0, x1, y1):
    vline (x0, y0, x1, y1, "stoneWallTop", "_E")

def short_wall_w (x0, y0, x1, y1):
    vline (x0, y0, x1, y1, "stoneWallTop", "_W")

#
#  stone archway
#

def archway_n (x, y):
    place_named_glyph (x, y, "stoneWallArchway", "_N")

def archway_s (x, y):
    place_named_glyph (x, y, "stoneWallArchway", "_S")

def archway_e (x, y):
    place_named_glyph (x, y, "stoneWallArchway", "_E")

def archway_w (x, y):
    place_named_glyph (x, y, "stoneWallArchway", "_W")

#
#  stone wall and column
#

def wall_column_n (x, y):
    place_named_glyph (x, y, "stoneWallColumnIn", "_N")

def wall_column_s (x, y):
    place_named_glyph (x, y, "stoneWallColumnIn", "_S")

def wall_column_e (x, y):
    place_named_glyph (x, y, "stoneWallColumnIn", "_E")

def wall_column_w (x, y):
    place_named_glyph (x, y, "stoneWallColumnIn", "_W")

#
#  narrow doorway open
#

def narrow_open_n (x, y):
    place_named_glyph (x, y, "stoneWallDoorOpen", "_N")

def narrow_open_s (x, y):
    place_named_glyph (x, y, "stoneWallDoorOpen", "_S")

def narrow_open_e (x, y):
    place_named_glyph (x, y, "stoneWallDoorOpen", "_E")

def narrow_open_w (x, y):
    place_named_glyph (x, y, "stoneWallDoorOpen", "_W")

#
#  narrow doorway closed
#

def narrow_closed_n (x, y):
    place_named_glyph (x, y, "stoneWallDoorClosed", "_N")

def narrow_closed_s (x, y):
    place_named_glyph (x, y, "stoneWallDoorClosed", "_S")

def narrow_closed_e (x, y):
    place_named_glyph (x, y, "stoneWallDoorClosed", "_E")

def narrow_closed_w (x, y):
    place_named_glyph (x, y, "stoneWallDoorClosed", "_W")

#
#  wide doorway open
#

def wide_open_n (x, y):
    place_named_glyph (x, y, "stoneWallGateOpen", "_N")

def wide_open_s (x, y):
    place_named_glyph (x, y, "stoneWallGateOpen", "_S")

def wide_open_e (x, y):
    place_named_glyph (x, y, "stoneWallGateOpen", "_E")

def wide_open_w (x, y):
    place_named_glyph (x, y, "stoneWallGateOpen", "_W")

#
#  wide doorway closed
#

def wide_closed_n (x, y):
    place_named_glyph (x, y, "stoneWallGateClosed", "_N")

def wide_closed_s (x, y):
    place_named_glyph (x, y, "stoneWallGateClosed", "_S")

def wide_closed_e (x, y):
    place_named_glyph (x, y, "stoneWallGateClosed", "_E")

def wide_closed_w (x, y):
    place_named_glyph (x, y, "stoneWallGateClosed", "_W")


#
#  window open
#

def window_n (x, y):
    place_named_glyph (x, y, "stoneWallWindow", "_N")

def window_s (x, y):
    place_named_glyph (x, y, "stoneWallWindow", "_S")

def window_e (x, y):
    place_named_glyph (x, y, "stoneWallWindow", "_E")

def window_w (x, y):
    place_named_glyph (x, y, "stoneWallWindow", "_W")

#
#  window bars
#

def window_bars_n (x, y):
    place_named_glyph (x, y, "stoneWallWindowBars", "_N")

def window_bars_s (x, y):
    place_named_glyph (x, y, "stoneWallWindowBars", "_S")

def window_bars_e (x, y):
    place_named_glyph (x, y, "stoneWallWindowBars", "_E")

def window_bars_w (x, y):
    place_named_glyph (x, y, "stoneWallWindowBars", "_W")

#
#  floors
#

def floor_n (x, y):
    place_named_glyph (x, y, "stoneUneven", "_N")

def floor_s (x, y):
    place_named_glyph (x, y, "stoneUneven", "_S")

def floor_e (x, y):
    place_named_glyph (x, y, "stoneUneven", "_E")

def floor_w (x, y):
    place_named_glyph (x, y, "stoneUneven", "_W")

def floor_tile_n (x, y):
    place_named_glyph (x, y, "stoneTile", "_N")

def floor_tile_s (x, y):
    place_named_glyph (x, y, "stoneTile", "_S")

def floor_tile_e (x, y):
    place_named_glyph (x, y, "stoneTile", "_E")

def floor_tile_w (x, y):
    place_named_glyph (x, y, "stoneTile", "_W")

floors = {0: floor_n,
          1: floor_s,
          2: floor_e,
          3: floor_w,
          4: floor_tile_n,
          5: floor_tile_s,
          6: floor_tile_e,
          7: floor_tile_w}

def rand_floor (x, y):
    floors[random.randint (0, 3)] (x, y)

def all_floor ():
    for x in range (6):
        for y in range (6):
            rand_floor (x, y)

#
#  insert_glyph - insert glyph into the glyphs list.
#                pre-condition:  an initialised glyph, t.
#                post-condition:  t, is added at the list of glyphs.
#

def insert_glyph (t):
    global glyphs
    glyphs += [t]


def flush_glyphs ():
    global glyphs
    for t in glyphs:
        x = t.isometric[0]
        y = t.isometric[1]
        gameDisplay.blit (t.image, (x, y))
    glyphs = []
    pygame.display.flip ()


def gen_filename (subdir, filename):
    global prefix

    path = os.path.join (subdir, filename)
    if prefix != "":
        path = os.path.join (prefix, path)
    return path


#
#  load_png - loads the image and return image object
#

def load_png(name):
    fullname = gen_filename ('isoart', name + '.png')
    try:
        if os.path.isfile (fullname):
            # os.system ('convert ' + fullname + ' -trim output.png')
	    # image = pygame.image.load ('output.png')
            image = pygame.image.load (fullname)
            image = pygame.transform.scale (image, (unitX, unitY))
	    if image.get_alpha() is None:
	        return image.convert ()
	    else:
	        return image.convert_alpha ()
        else:
            fatal_error ('image does not exist: %s\n', fullname)
    except pygame.error, message:
        fatal_error ('image does not exist: %s\n', fullname)


#
#  get_image - return the image
#

def get_image (name):
    global images
    if not images.has_key (name):
        images[name] = load_png (name)
    return images[name]


#
#  pause - wait for escape to be pressed before exiting.
#

def pause ():
    while True:
        event = pygame.event.wait ()
        if (event.type == KEYUP) or (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                sys.exit(0)


#
#  clear_screen
#

def clear_screen ():
    global gameDisplay
    gameDisplay.fill (Black)


"""
def grid (msec):
    for x in range (20):
        clear_screen ()
        # all_floor ()
        hwall (0, 0, x, 0)
        # wall (x, 0, x, 10)
        # wall (x-1, 10, 0, 10)
        # wall (0, 10, 0, 0)
        pygame.time.delay (msec)
        flush_glyphs ()
    for x in range (20):
        for y in range (20):
            vwall (x, 0, x, y)
            pygame.time.delay (msec)
            flush_glyphs ()
"""


def square (amount):
    corner_n (0, 0)
    aged_wall_w (0, 1, 0, amount)
    window_bars_s (0, amount)
    wide_closed_s (1, amount)
    window_bars_s (2, amount)
    # broken_wall_left_s (0, amount)
    aged_wall_s (3, amount, amount, amount)
    aged_wall_n (amount-1, 0, 1, 0)
    corner_e (amount, 0)
    aged_wall_e (amount, amount, amount-1, 0)
    narrow_closed_e (amount, amount)


def grid ():
    midx = unitX * numberOfTilesInX / 2.0
    for x in range (12):
        pygame.draw.rect (gameDisplay, White, [midx + unitX * x * 2, 0, 1, 24 * unitY], 0)
        pygame.draw.rect (gameDisplay, White, [midx - unitX * x * 2, 0, 1, 24 * unitY], 0)
    offsetx = (mapAreaX - unitX * 24 * 2) / 2.0
    for y in range (24):
        pygame.draw.rect (gameDisplay, White, [offsetx, y * unitY, 24 * unitX * 2, 2], 0)
    pygame.display.flip ()


def testISO (msec):
    clear_screen ()
    # grid ()
    all_floor ()
    flush_glyphs ()

    for s in range (4):
        clear_screen ()
        all_floor ()
        # grid ()
        # pause ()
        square (s)
        flush_glyphs ()
        pygame.time.delay (msec*80)

    pause ()


#
#  init -
#

def init (resolution = default_resolution, fullscreen = True):
    global gameDisplay

    pygame.init ()
    if fullscreen:
        gameDisplay = pygame.display.set_mode (resolution, FULLSCREEN)
    else:
        gameDisplay = pygame.display.set_mode (resolution)
        pygame.display.set_caption ('Penguin Tower')
    pygame.mouse.set_visible (False)


def main():
    redraw (redraw_method)
    init ()
    testISO (10)



#
#  call main if we are testing this module
#

if __name__ == '__main__':
    main ()
