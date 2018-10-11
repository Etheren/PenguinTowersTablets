#!/usr/bin/env python

import isometric


def main ():
    isometric.init ()
    isometric.clear ()
    isometric.wall (1, 1, 1, 10)
    isometric.wall (1, 10, 10, 10)
    isometric.wall (10, 10, 10, 1)
    isometric.wall (10, 1, 1, 1)
    isometric.draw_player (5, 5, isometric.north)
    isometric.closed_door (1, 2, 1, 3)
    isometric.render_room ()


main ()
