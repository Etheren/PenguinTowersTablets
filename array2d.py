#!/usr/bin/env python

# Copyright (C) 2017
#               Free Software Foundation, Inc.
# This file is part of Chisel.
#
# Chisel is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# Chisel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chisel; see the file COPYING.  If not, write to the
# Free Software Foundation, 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Author Gaius Mulley <gaius@gnu.org>
#


class array2d:
    #
    #  __init__ - populate a 2d contents list of y rows of x columns
    #             each cell is a value.
    #

    def __init__ (self, x, y, value):
        self._initvalue = value
        self._contents = []
        self.x = 0
        self.y = 0
        self._grow (x, y, value)

    #
    #  grow - expand the 2d contents to x, y using value content.
    #

    def _grow (self, x, y, value = None):
        if (x >= self.x) or (y >= self.y):
            if value == None:
                value = self._initvalue
            n = []
            if x > self.x:
                for j in self._contents:
                    n += [j + (x - self.x)*value]
                self.x = x
            else:
                for j in self._contents:
                    n += [j]
            self._contents = n
            if y > self.y:
                r = [value*self.x]
                self._contents += r * (y-self.y)
                self.y = y


    #
    #  cut - given a list, l, return a triple
    #        containing elements:  <i, i, >i
    #        if i is at the end of the list None
    #        is returned.
    #

    def _cut (self, l, i):
        if len (l) < i:
            print "internal error in array2d.cut (l =", l, "len (l) =", len (l), "i =", i
        if i == 0:
            if len (l) > 1:
                return None, l[i], l[i+1:]
            return None, l[i], None
        if len (l) > i+1:
            return l[:i], l[i], l[i+1:]
        return l[:i], l[i], None

    #
    #  stitch - returns [a+b+c]
    #           where a, b and c are either a list or None.
    #

    def _stitch (self, a, b, c):
        if a == None:
            d = b
        else:
            d = a + b
        if c == None:
            return d
        return d + c

    #
    #  set - set array [x, y] to value
    #

    def set (self, x, y, value):
        self._grow (x+1, y+1)
        a, b, c = self._cut (self._contents, y)
        x, y, z = self._cut (b, x)
        b = self._stitch (x, value, z)
        self._contents = self._stitch (a, [b], c)

    #
    #  get - get value held at position, [x, y]
    #

    def get (self, x, y):
        self._grow (x+1, y+1)
        return self._contents[y][x]

    #
    #  high - return the maximum indices in the 2d array.
    #

    def high (self):
        return [self.x, self.y]

    #
    #  inRange - return True if, x, y can index into the array.
    #

    def inRange (self, x, y):
        h = self.high ()
        return (x >= 0) and (x < h[0]) and (y >= 0) and (y < h[1])
