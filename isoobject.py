#!/usr/bin/env python

import sys, os, pygame, random, array2d
from pygame.locals import *
from chvec import *


numberOfTilesInX = 10

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

contents           = []   #  high level description of the room characteristics
bricks             = []   #  bricks of length 1, 2, 3 and 4 units.
use_brick_optimizer= True
screen_angle       = 0
# rotation_point     = [int (numberOfTilesInX / 2), int (numberOfTilesInX / 2)]
rotation_point     = [10, 10]
orientation        = {0: "_N", 90: "_W", 180: "_S", 270: "_E"}


def rotate_point (angle, p):
    if angle == 0:
        return p
    pox = p[0] - rotation_point[0]
    poy = p[1] - rotation_point[1]

    if angle == 90:
        x, y = -poy, pox
    elif angle == 180:
        x, y = -pox, -poy
    elif angle == 270:
        x, y = poy, -pox
    return [x + rotation_point[0], y + rotation_point[1]]


def rotate_object (angle, c):
    if is_wall (c) or is_door (c):
        return [c[0], sort_coords (rotate_point (angle, c[1][0]),
                                   rotate_point (angle, c[1][1]))]
    return [c[0], rotate_point (angle, c[1])]


def rotate_contents (angle):
    global contents
    if angle != 0:
        #print contents
        #print "rotate the contents by", angle
        new_contents = []
        for c in contents:
            new_contents += [rotate_object (angle, c)]
        contents = new_contents
        #print contents
        render_screen ()


def render_screen ():
    clear_screen ()
    all_floor ()
    flush_glyphs ()
    render_room ()
    if use_brick_optimizer:
        optimize_bricks ()
    flush_bricks ()
    flush_glyphs ()


def screen_orientation (degrees):
    global screen_angle
    diff = (screen_angle - degrees + 360) % 360
    screen_angle = degrees
    rotate_contents (diff)


#
#  simple_controls -
#

def simple_controls ():
    while True:
        event = pygame.event.wait ()
        if (event.type == KEYUP) or (event.type == KEYDOWN):
            if event.key == K_ESCAPE:
                sys.exit (0)
        if event.type == KEYDOWN:
            if event.key == K_UP:
                screen_orientation (0)
            elif event.key == K_DOWN:
                screen_orientation (180)
            elif event.key == K_RIGHT:
                screen_orientation (270)
            elif event.key == K_LEFT:
                screen_orientation (90)


#
#  testPen - scratch test
#

def testPen ():

    """
    wall (1, 1, 1, 10)
    wall (1, 10, 10, 10)
    wall (10, 10, 10, 1)
    wall (10, 1, 1, 1)
    closed_door (1, 2, 1, 3)
    closed_door (2, 10, 3, 10)
    """

    wall (1, 1, 1, 6)
    wall (1, 1, 6, 1)

    wall (1, 1, 1, 6)
    wall (1, 6, 7, 6)
    wall (1, 1, 16, 1)
    wall (7, 9, 10, 9)
    wall (10, 19, 16, 19)
    wall (10, 9, 10, 19)
    wall (16, 1, 16, 19)
    wall (7, 6, 7, 9)
    open_door (16, 16, 16, 17)
    closed_door (12, 19, 13, 19)
    open_door (10, 17, 10, 18)
    closed_door (16,  9, 16, 10)

    barrel (20, 20)

    open_chest (18, 1)
    """
    barrel (3, 5)
    barrel (2, 4)
    barrel (10, 10)
    # barrel (11, 11)
    # closed_chest (2, 4)
    """

    render_screen ()
    simple_controls ()


#
#  testRoom - create a test room
#

def testRoom ():

    """
    wall (1, 1, 1, 10)
    wall (1, 10, 10, 10)
    wall (10, 10, 10, 1)
    wall (10, 1, 1, 1)
    closed_door (1, 2, 1, 3)
    closed_door (2, 10, 3, 10)
    """

    wall (1, 1, 1, 6)
    wall (1, 1, 6, 1)

    wall (1, 1, 1, 6)
    wall (1, 6, 7, 6)
    wall (1, 1, 16, 1)
    wall (7, 9, 10, 9)
    wall (10, 19, 16, 19)
    wall (10, 9, 10, 19)
    wall (16, 1, 16, 19)
    wall (7, 6, 7, 9)
    open_door (16, 16, 16, 17)
    closed_door (12, 19, 13, 19)
    open_door (10, 17, 10, 18)
    closed_door (16,  9, 16, 10)

    barrel (20, 20)

    open_chest (18, 1)
    """
    barrel (3, 5)
    barrel (2, 4)
    barrel (10, 10)
    # barrel (11, 11)
    # closed_chest (2, 4)
    """
    render_screen ()


#
#  get_next_wall - returns the next wall which connects with, last_pos.
#                  pre-condition:  contents is a list of walls and doors
#                  post-condition: a wall is selected and removed from contents
#                                  this wall will either start or end on last_pos.
#                                  None is returned if no wall is found.
#

def get_next_wall (last_pos):
    global contents
    i = 0
    while i < len (contents):
        if contents[i][0] == 'wall':
            if (last_pos == None) or equVec (last_pos, contents[i][1][0]) or equVec (last_pos, contents[i][1][1]):
                w = contents[i]
                w = [w[0], sort_coords (w[1][0], w[1][1])]
                del contents[i]
                return w
        i += 1
    return None


def do_render_wall (start_pos, end_pos, completed_room, horizontal):
    if start_pos == None:
        return completed_room
    completed_room += [["wall", [start_pos, end_pos]]]
    line (horizontal, start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    #print "wall line", start_pos, end_pos
    return completed_room


#
#  is_door - returns True if contents, c, represents a door.
#

def is_door (c):
    return (c[0] == "open") or (c[0] == "secret") or (c[0] == "closed")


#
#  is_wall - returns True if contents, c, represents a wall.
#

def is_wall (c):
    return c[0] == "wall"


#
#  is_barrel - returns True if contents, c, represents a barrel.
#

def is_barrel (c):
    return c[0] == "barrel"


#
#  is_openchest - returns True if contents, c, represents an open chest.
#

def is_openchest (c):
    return c[0] == "openchest"


#
#  is_closedchest - returns True if contents, c, represents a closed chest.
#

def is_closedchest (c):
    return c[0] == "closedchest"


#
#  is_horizontal - return True is the contents is horizontal.
#

def is_horizontal (c):
    return isHorizontal (c[1][0][0], c[1][0][1], c[1][1][0], c[1][1][1])


#
#  is_vertical - return True is the contents is vertical.
#

def is_vertical (c):
    return isVertical (c[1][0][0], c[1][0][1], c[1][1][0], c[1][1][1])


#
#  is_subrange - pre-condition:  d and w are contents lists.
#                post-condition:  returns True if d is a subrange of, w.
#

def is_subrange (w, d):
    if (w[1][0][1] == w[1][1][1]) and (d[1][0][1] == d[1][1][1]) and (w[1][0][1] == d[1][1][1]):
        return (d[1][0][0] > w[1][0][0]) and (d[1][1][0] < w[1][1][0])
    if (w[1][0][0] == w[1][1][0]) and (d[1][0][0] == d[1][1][0]) and (w[1][0][0] == d[1][1][0]):
        return (d[1][0][1] > w[1][0][1]) and (d[1][1][1] < w[1][1][1])
    return False


#
#  get_doors_on_wall - pre-condition:  w is a wall content list.
#                      post-condition:  all doors on this wall are returned as a list.
#

def get_doors_on_wall (w):
    doors = []
    for c in contents:
        if is_door (c) and is_subrange (w, c):
            doors += [c]
    return doors


#
#  do_render_door - pre-condition:
#                   post-condition:
#

def do_render_door (d, horizontal):
    if horizontal:
        if d[0] == "closed":
            place_glyph (d[1][0][0], d[1][0][1], 3, "stoneWallDoorClosed", "_N")
        elif d[0] == "open":
            place_glyph (d[1][0][0], d[1][0][1], 3, "stoneWallDoorOpen", "_N")
    else:
        if d[0] == "closed":
            place_glyph (d[1][0][0], d[1][0][1], 3, "stoneWallDoorClosed", "_W")
        elif d[0] == "open":
            place_glyph (d[1][0][0], d[1][0][1], 3, "stoneWallDoorOpen", "_W")


#
#  build_horiz_wall -
#

def build_horiz_wall (c, completed_room):
    start_pos = None
    last_pos = None
    #print "completed_room", completed_room
    for x in range (c[1][0][0], c[1][1][0]+1):
        #print "horiz: wall position", x, c[1][0][1],
        if is_on (x, c[1][0][1], completed_room):
            #print "already present", x, c[1][0][1], "is on", completed_room
            # finished this wall segment
            completed_room = do_render_wall (start_pos, last_pos, completed_room, True)
            start_pos = None
            last_pos = None
        else:
            #print "will be added"
            last_pos = [x, c[1][0][1]]
            if start_pos == None:
                start_pos = [x, c[1][0][1]]
    return do_render_wall (start_pos, last_pos, completed_room, True)


#
#  build_vert_wall -
#

def build_vert_wall (c, completed_room):
    start_pos = None
    last_pos = None
    for y in range (c[1][0][1], c[1][1][1]+1):
        #print "vert: wall position", c[1][0][0], y
        if is_on (c[1][0][0], y, completed_room):
            # finished this wall segment
            completed_room = do_render_wall (start_pos, last_pos, completed_room, False)
            start_pos = None
            last_pos = None
        else:
            last_pos = [c[1][0][0], y]
            if start_pos == None:
                start_pos = [c[1][0][0], y]
    return do_render_wall (start_pos, last_pos, completed_room, False)


#
#  in_range - return True if, x, is in the range a..b
#

def in_range (a, b, x):
    return (a <= x) and (b >= x)


#
#  is_point_on - return True if x, y, is on line, c.
#

def is_point_on (x, y, c):
    if is_vertical (c) and (x == c[1][0][0]) and in_range (c[1][0][1], c[1][1][1], y):
        return True
    if is_horizontal (c) and (y == c[1][0][1]) and in_range (c[1][0][0], c[1][1][0], x):
        return True
    return False


#
#  is_on - returns True if point, x, y, is on wall or door list, l.
#

def is_on (x, y, l):
    for c in l:
        if is_point_on (x, y, c):
            return True
    return False


#
#
#

def render_doors ():
    completed_room = []
    for w in contents:
        if is_wall (w):
            if is_horizontal (w):
                for d in get_doors_on_wall (w):
                    new_door = [d[0], [addVec (d[1][0], [-1, 0]), addVec (d[1][1], [1, 0])]]
                    do_render_door (new_door, True)
                    completed_room += [new_door]
            else:
                for d in get_doors_on_wall (w):
                    new_door = [d[0], [addVec (d[1][0], [0, -1]), addVec (d[1][1], [0, 1])]]
                    do_render_door (new_door, False)
                    completed_room += [new_door]
    return completed_room


#
#  render_room_internals -
#

def render_room_internals ():
    for c in contents:
        if is_barrel (c):
            place_glyph (c[1][0], c[1][1], 3, "barrel", orientation[screen_angle])
        elif is_openchest (c):
            place_glyph (c[1][0], c[1][1], 3, "chestOpen", orientation[screen_angle])
        elif is_closedchest (c):
            place_glyph (c[1][0], c[1][1], 3, "chestClosed", orientation[screen_angle])


#
#  render_room - pre-condition:
#                post-condition:
#

def render_room ():
    render_room_internals ()
    completed_room = render_doors ()
    #print "contents =", contents
    for c in contents:
        #print "completed_room", completed_room
        if is_wall (c):
            #print "adding wall", c
            if is_horizontal (c):
                completed_room = build_horiz_wall (c, completed_room)
            else:
                completed_room = build_vert_wall (c, completed_room)


#
#  cart2iso - pre-condition:  x, y, z are cartesian coordinates.
#             post-condition:  x, y, z, are mapped into their isometric positions.
#

def cart2iso (x, y, z, xscale, yscale, xoffset, yoffset):
    cx = unitX * numberOfTilesInX / 2.0 + ((x - y) * xscale * unitX) / 2.0 + xoffset * unitX

    # print "unitX =", unitX, "unitY =", unitY,
    # print "numberOfTilesInX =", numberOfTilesInX, x, y,
    cx = (unitX * numberOfTilesInX / 2.0 + ((x - y) * xscale * unitX) / 8.0 + xoffset * unitX)
    cy = ((x + y) * unitY * yscale + yoffset * unitY) / 4
    # print "cx, cy =", cx, cy
    #
    #  the isometric z value is the furthest point down the screen for the iso tile
    #  (visually nearer the viewer).
    #
    return cx, cy, cy+z


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
    # sys.exit (1)


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
#
#

def place_glyph (x, y, z, basename, orientation):
    s = get_family (basename + orientation)
    t = glyph (x, y, z, s[0], s[1], s[2], s[3]).set_image (get_image (basename + orientation))
    insert_glyph (t)


#
#  add_wall_segment - record the wall segment in a list, bricks.
#

def add_wall_segment (x, y, z, length, orientation, basename, extension):
    global bricks
    bricks += [[x, y, z, length, orientation, basename, extension]]


def get_brick_pos (b):
    global bricks
    return [bricks[b][0], bricks[b][1]]


image_base = { 1: "stoneWallColumn",
               2: "stoneWall2Aged",
               3: "stoneWall3Aged",
               4: "stoneWallAged" }


#
#
#

def replace_add_wall_segment (unit, other, x, y, z, length, orientation, basename, extension):
    global bricks
    add_wall_segment (x, y, z, length, orientation, basename, extension)
    if unit > other:
        del bricks[unit]
        del bricks[other]
    else:
        del bricks[other]
        del bricks[unit]


#
#  have_combined - if brick, unit, is next to brick other
#                  then combine unit with other and return True
#                  else return False
#

def have_combined (unit, other):
    global bricks
    if unit != other:
        #print "unit =", unit, bricks[unit], "other =", other, bricks[other]
        other_pos = get_brick_pos (other)
        other_len = bricks[other][3]
        unit_pos = get_brick_pos (unit)
        if (bricks[other][4] == 'horizontal') or (other_len == 1):
            inc_unit = [1, 0]
            if equVec (subVec (other_pos, inc_unit), unit_pos):
                replace_add_wall_segment (unit, other, unit_pos[0], unit_pos[1], other_len, other_len+1, "horizontal", image_base[other_len + 1], "_N")
                return True
            if equVec (addVec (other_pos, inc_unit), unit_pos):
                replace_add_wall_segment (unit, other, other_pos[0], other_pos[1], other_len, other_len+1, "horizontal", image_base[other_len + 1], "_N")
                return True
        if (bricks[other][4] == 'vertical') or (other_len == 1):
            inc_unit = [0, 1]
            if equVec (subVec (other_pos, inc_unit), unit_pos):
                replace_add_wall_segment (unit, other, unit_pos[0], unit_pos[1], other_len, other_len+1, "vertical", image_base[other_len + 1], "_W")
                return True
            if equVec (addVec (other_pos, inc_unit), unit_pos):
                replace_add_wall_segment (unit, other, other_pos[0], other_pos[1], other_len, other_len+1, "vertical", image_base [other_len + 1], "_W")
                return True
    return False


#
#  optimize_bricks -
#

def optimize_bricks ():
    global bricks
    changed = True
    while changed:
        changed = False
        i = 0
        while (not changed) and (i < len (bricks)):
            if bricks[i][3] == 1:
                j = 0
                while (not changed) and (j < len (bricks)):
                    if (bricks[j][3] < 4) and have_combined (i, j):
                        changed = True
                    else:
                        j += 1
            i += 1
    #print bricks


#
#
#

def flush_bricks ():
    global bricks
    for b in bricks:
        place_glyph (b[0], b[1], b[2], b[5], b[6])
    bricks = []


#
#  hlineopt - minimise the horizontal tiles used (minimise the joins)
#

def hlineopt (x0, y0, x1, y1):
    xstart = min (x0, x1)
    xend = max (x0, x1)
    x = xstart
    while x <= xend:
        if abs (x-xend) > 3:
            add_wall_segment (x, y0, 3, 4, "horizontal", "stoneWallAged", "_N")
            x += 4
        elif abs (x-xend) == 3:
            add_wall_segment (x, y0, 2, 3, "horizontal", "stoneWall3Aged", "_N")
            x += 3
        elif abs (x-xend) == 2:
            add_wall_segment (x, y0, 1, 2, "horizontal", "stoneWall2Aged", "_N")
            x += 2
        else:
            add_wall_segment (x, y0, 0, 1, "horizontal", "stoneWallColumn", "_N")
            x += 1


#
#  vlineopt - minimise the horizontal tiles used (minimise the joins)
#

def vlineopt (x0, y0, x1, y1):
    ystart = min (y0, y1)
    yend = max (y0, y1)
    y = ystart
    while y <= yend:
        if abs (y-yend) > 3:
            add_wall_segment (x0, y, 3, 4, "vertical", "stoneWallAged", "_W")
            y += 4
        elif abs (y-yend) == 3:
            add_wall_segment (x0, y, 2, 3, "vertical", "stoneWall3Aged", "_W")
            y += 3
        elif abs (y-yend) == 2:
            add_wall_segment (x0, y, 1, 2, "vertical", "stoneWall2Aged", "_W")
            y += 2
        else:
            add_wall_segment (x0, y, 0, 1, "vertical", "stoneWallColumn", "_N")
            y += 1


#
#  line - draw a vertical or horizontal line of images.
#

def line (horizontal, x0, y0, x1, y1):
    if horizontal:
        hlineopt (x0, y0, x1, y1)
    else:
        vlineopt (x0, y0, x1, y1)


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
#  sort_coords - sort the two coord, a, and, b, so that horizontal line,
#                x, values are in ascending order.  Or a vertical line the y
#                values are in ascending order.
#

def sort_coords (a, b):
    if isHorizontal (a[0], a[1], b[0], b[1]):
        if a[0] > b[0]:
            return [b, a]
    else:
        if a[1] > b[1]:
            return [b, a]
    return [a, b]


#
#  barrel - places a single barrel at position, x, y.
#           In penguin tower are vertical or horizontal only.
#

def barrel (x, y):
    global contents
    contents += [["barrel", [x, y]]]

#
#  open_chest - places a single open chest at position, x, y.
#               In penguin tower are vertical or horizontal only.
#

def open_chest (x, y):
    global contents
    contents += [["openchest", [x, y]]]


#
#  chest_closed - places a single closed chest at position, x, y.
#                 In penguin tower are vertical or horizontal only.
#

def closed_chest (x, y):
    global contents
    contents += [["closedchest", [x, y]]]


#
#  wall - creates a wall object in the scene.  The walls in penguin tower are
#         vertical or horizontal only.
#         pre-condition:
#

def wall (x0, y0, x1, y1):
    global contents
    contents += [["wall", sort_coords ([x0, y0], [x1, y1])]]


#
#  closed_door - creates a closed door object in the scene.  The doors
#                in penguin tower are vertical or horizontal only.
#

def closed_door (x0, y0, x1, y1):
    global contents
    contents += [["closed", sort_coords ([x0, y0], [x1, y1])]]


#
#  open_door - creates an open door object in the scene.  The doors
#              in penguin tower are vertical or horizontal only.
#

def open_door (x0, y0, x1, y1):
    global contents
    contents += [["open", sort_coords ([x0, y0], [x1, y1])]]


#
#  secret_door - creates a secret door object in the scene.  The doors
#                in penguin tower are vertical or horizontal only.
#

def secret_door (x0, y0, x1, y1):
    global contents
    contents += [["secret", sort_coords ([x0, y0], [x1, y1])]]


#
#  inside - square, x, y is inside the room.
#

def inside (x, y):
    global contents
    contents += [["inside", [x, y]]]


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

def column_n (x, y):
    place_named_glyph (x, y, "stoneWallColumn", "_N")

def column_s (x, y):
    place_named_glyph (x, y, "stoneWallColumn", "_S")

def column_e (x, y):
    place_named_glyph (x, y, "stoneWallColumn", "_E")

def column_w (x, y):
    place_named_glyph (x, y, "stoneWallColumn", "_W")

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
    for x in range (0, 6*4, 4):
        for y in range (0, 6*4, 4):
            rand_floor (x, y)

#
#  insert_glyph - insert glyph into the glyphs list.
#                 pre-condition:  an initialised glyph, t.
#                 post-condition:  t, is added at the list of glyphs in ascending, z, order.
#

def insert_glyph (t):
    global glyphs
    if glyphs == []:
        glyphs = [t]
        return
    i = 0
    while i < len (glyphs):
        # print glyphs[i].isometric[2], t.isometric[2]
        if glyphs[i].isometric[2] > t.isometric[2]:
            #
            #  t must be inserted before position, i.
            #
            if i == 0:
                glyphs = [t] + glyphs
            else:
                glyphs = glyphs[:i] + [t] + glyphs[i:]
            return
        i += 1
    glyphs += [t]


def flush_glyphs ():
    global glyphs
    for t in glyphs:
        x = t.isometric[0]
        y = t.isometric[1]
        gameDisplay.blit (t.image, (x, y))
    glyphs = []
    # pygame.display.flip ()


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


def testUnit (msec):
    """
    clear_screen ()
    all_floor ()
    flush_glyphs ()
    """

    """
    line (2, 10, 10, 10)
    line (1, 1, 10, 1)
    line (1, 2, 1, 10)
    line (10, 2, 10, 10)

    flush_glyphs ()
    pause ()

    """

    testPen ()


def set_display (display, width, height):
    global gameDisplay

    gameDisplay = display
    if (width != default_resolution[0]) or (height != default_resolution[1]):
        fatal_error ("currently the width/height must be set to 1290x1080\n")

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
    init ()
    # testISO (10)
    testUnit (10)
    # testPen ()


#
#  call main if we are testing this module
#

if __name__ == '__main__':
    main ()
