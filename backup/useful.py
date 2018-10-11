#
#  incl_string - includes string, name, in list, s.
#

def incl_string (s, name):
    for word in s:
        if word == name:
            return s
    return s + [name]


#
#  incl_square - includes, name, at position, x, y.
#

def incl_square (x, y, name):
    s = squares.get_square (x, y)
    s = incl_string (s, name)
    squares.set_square (x, y, s)


def is_odd (x):
    return (x % 2) == 1

def is_even (x):
    return (x % 2) == 0

def redraw_method (x, y):
    print x, y

#
#  redraw - use a brute force painters algorithm to redraw the screen.
#

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
#  int_list - return an integer list generated from, args.
#

def int_list (args):
    l = []
    for a in args:
        l += [int (a)]
    return l


#
#  sort_coords - sort the two coord, c[0] and c[1] so that horizontal line,
#                x, values are in ascending order.  Or a vertical line the y
#                values are in ascending order.
#

def sort_coords (c):
    if isHorizontal (c):
        if c[0][0] > c[1][0]:
            return [c[1], c[0]]
    else:
        if c[0][1] > c[1][1]:
            return [c[1], c[0]]
    return [c[0], c[1]]


#
#  do_render_wall -
#

def do_render_wall (l):
    global viewroom
    if isHorizontal (l):
        for y in range (l[0][1], l[1][1]+1):
            viewroom.set (l[0][0], y, '#')
    else:
        for x in range (l[0][0], l[1][0]+1):
            viewroom.set (x, l[0][1], '#')

#
#  isSinglePoint - return True if both coordinates are the same
#

def isSinglePoint (l):
    return (l[0][0] == l[1][0]) and (l[0][1] == l[1][1])


def isWall (c):
    return c[0] == "wall"


def onHorizontalWall (l):
    for c in contents:
        if isWall (c):
            if isIntersection (c[1:], c):
                return True
    return False

#
#  do_render_open -
#

def do_render_open (l):
    global viewroom

    if isSinglePoint (l):
        if onHorizontalWall (l):
            viewroom.set (l[0][0], y, '+')
        else:
            viewroom.set (l[0][0], y, '*')
    if isHorizontal (l):
        for y in range (l[0][1], l[1][1]+1):
            viewroom.set (l[0][0], y, '+')
    else:
        for x in range (l[0][0], l[1][0]+1):
            viewroom.set (x, l[0][1], '*')


#
#  do_render_closed -
#

def do_render_closed (l):
    global viewroom
    if isHorizontal (l):
        for y in range (l[0][1], l[1][1]+1):
            viewroom.set (l[0][0], y, '-')
    else:
        for x in range (l[0][0], l[1][0]+1):
            viewroom.set (x, l[0][1], '|')


#
#  do_render_secret -
#

def do_render_secret (l):
    global viewroom
    if isHorizontal (l):
        for y in range (l[0][1], l[1][1]+1):
            viewroom.set (l[0][0], y, ':')
    else:
        for x in range (l[0][0], l[1][0]+1):
            viewroom.set (x, l[0][1], '=')

def render_inside (l):
    pass

#
#  render_wall -
#

def render_wall (args):
    l = sort_coords (int_list (args))
    do_render_wall (l)

render_content = {"wall": render_wall,
                  "closed": do_render_closed,
                  "open": do_render_open,
                  "secret": do_render_secret,
                  "inside": render_inside}

def render_room ():
    global viewroom, view_maxx, view_maxy
    viewroom = array2d.array2d (1, 1, "")
    view_maxx, view_maxy = 0, 0
    for c in contents:
        render_content[c[0]] (c[1:])
