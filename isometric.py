#!/usr/bin/env python


floor = []
walls = []
doors = []
items = []
player = []
opponents = []
debugging = True


#
#  _printf - keeps C programmers happy :-)
#

def _printf (format, *args):
    print str (format) % args,


#
#  _debugf - _printf when debugging is True
#

def _debugf (format, *args):
    global debugging

    if debugging:
        print str (format) % args,

#
#  _errorf - generate an error associated with pge and raise an exception.
#

def _errorf (format, *args):
    m = str (format) % args
    sys.stdout.write ("isometric: " + m)
    sys.exit (1)


def clear ():
    global floor, walls, doors, items, player, opponents
    floor = []
    walls = []
    doors = []
    items = []
    player = []
    opponents = []


#
#  wall - places a wall, x0, y0, x1, y1 into the walls list.
#

def wall (x0, y0, x1, y1):
    global walls
    walls += [[x0, y0, x1, y1]]


#
#  open_door - places an open door, x0, y0, x1, y1 into the doors list.
#

def open_door (x0, y0, x1, y1):
    global doors
    doors += [[x0, y0, x1, y1, "open"]]


#
#  closed_door - places a closed door, x0, y0, x1, y1 into the doors list.
#

def closed_door (x0, y0, x1, y1):
    global doors
    doors += [[x0, y0, x1, y1, "closed"]]


#
#  secret_door - places a secret door, x0, y0, x1, y1 into the doors list.
#

def secret_door (x0, y0, x1, y1):
    global doors
    doors += [[x0, y0, x1, y1, "secret"]]


#
#
#

def draw_player (x, y, direction):
    global player
    player = [x, y, direction]


def draw_opponent (x, y, direction):
    global opponents
    opponents += [x, y, direction]


def callfunc (p):
    pass

#
#  render_room - renders the room which has so far been described by the above calls.
#

def render_room ():
    if player == []:
        _errorf ("the player position must be known before a room can be rendered")
    for p in generate_floor_plan_orientation ():
        callfunc (p)
