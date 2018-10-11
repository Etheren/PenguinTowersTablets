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
#  addVec - returns a new list containing the sum of the
#           elements in both indices.
#           It returns a+b of the two vectors.
#

def addVec (pos, vec):
    result = []
    for p, v in zip (pos, vec):
        result += [p+v]
    return result

#
#  subVec - returns a new list containing the subtraction
#           of the elements in both indices.
#           It returns a-b of the two vectors.
#

def subVec (a, b):
    result = []
    for p, v in zip (a, b):
        result += [p-v]
    return result


#
#  minVec - given two lists or vectors, a, b.
#           Return a new list containing the smallest
#           element in either indice or a and b.
#

def minVec (a, b):
    result = []
    for p, v in zip (a, b):
        result += [min (p, v)]
    return result


#
#  maxVec - given two lists or vectors, a, b.
#           Return a new list containing the largest
#           element in either indice or a and b.
#

def maxVec (a, b):
    result = []
    for p, v in zip (a, b):
        result += [max (p, v)]
    return result


#
#  equVec - return true if a == b.
#           We need to test each element of the vector (list).
#

def equVec (a, b):
    for i, j in zip (a, b):
        if i != j:
            return False
    return True

#
#
#

def intVec (v):
    r = []
    for i in v:
        r += [int (i)]
    return r
