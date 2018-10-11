#!/usr/bin/env python

debugging = False
debugging = True

import pygame
from pygame.locals import *
import hymnexec
import os

display_width = 800
display_height = 460

black = (0,0,0)
white = (255,255,255)
green = (100,200,0)
red   = (200,0,50)
blue  = (0,0,255)

wood_light = (166, 124, 54)
wood_dark = (76, 47, 0)

dark_red = (130, 30, 40)
dark_green = (25, 100, 50)
dark_blue = (25, 50, 150)

steel  = (128, 128, 128)
copper = (128, int (0.3 * 256.0), int (0.2 * 256.0))
gold   = (int (0.8 * 256.0), int (0.6 * 256.0), int (0.15 * 256.0))

active = None
hymn   = ["", "", ""]
index  = []
choices = []
service_choices = []
need_update = False
full_screen = not debugging

setup_form, service_form = range (2)
menu_form = setup_form

def read_index ():
    global index
    for l in open ("index", "r").readlines ():
        c = l.split ('#')[0]
        if c != '':
            index += [c]

def text_objects (text, font, colour = white):
    textSurface = font.render (text, True, colour)
    return textSurface, textSurface.get_rect ()

def message_display (text):
    largeText = pygame.font.Font (None, 115)
    TextSurf, TextRect = text_objects (text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit (TextSurf, TextRect)
    pygame.display.update ()
    time.sleep (2)

def button (clicked, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos ()
    click = pygame.mouse.get_pressed ()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect (gameDisplay, ac, (x, y, w, h))

        if clicked and action != None:
            action ()
    else:
        pygame.draw.rect (gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont (None, 100)
    textSurf, textRect = text_objects (msg, smallText, white)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit (textSurf, textRect)

def hymnchoice (clicked, x, y, w, h, ic, ac, n, action=None):
    global active
    mouse = pygame.mouse.get_pos ()
    click = pygame.mouse.get_pressed ()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect (gameDisplay, ac, (x, y, w, h))

        if clicked and action != None:
            active = n
            action (n)
    elif active == n:
        pygame.draw.rect (gameDisplay, ac, (x, y, w, h))
    else:
        pygame.draw.rect (gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont (None, 100)
    msg = hymn[n]
    if msg == "":
        msg = "- - -"

    textSurf, textRect = text_objects (msg, smallText, white)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit (textSurf, textRect)

def hymnno (n):
    global choices, need_update
    choices = get_choice (hymn[active])
    need_update = True

def myquit ():
    print "called quit"
    hymnexec.stop_play ()
    pygame.quit ()
    if not debugging:
        os.system ("sync ; shutdown -r now")
    quit ()

def unitX (v):
    return int (v * display_width)

def unitY (v):
    return int (v * display_height)

def posX (v):
    return int (v * display_width)

def posY (v):
    return display_height - unitY (v)

def add_text (c):
    global choices
    if active != None:
        if len (hymn[active]) < 3:
            hymn[active] += c
            choices = get_choice (hymn[active])

def enter ():
    pass

def delete ():
    global need_update, choices
    if active != None:
        if len (hymn[active]) > 0:
            hymn[active] = hymn[active][0:-1]
        else:
            hymn[active] = ""
        choices = get_choice (hymn[active])
        need_update = True

def zero ():
    add_text ("0")

def one ():
    add_text ("1")

def two ():
    add_text ("2")

def three ():
    add_text ("3")

def four ():
    add_text ("4")

def five ():
    add_text ("5")

def six ():
    add_text ("6")

def seven ():
    add_text ("7")

def eight ():
    add_text ("8")

def nine ():
    add_text ("9")

def get_choice (num):
    choices = []
    for n in index:
        if len (num) < len (n) and (num == n[:len (num)]):
            if not (n[len(num)] in choices):
                choices += [n[len(num)]]
    return choices

def keypad (clicked):
    num = hymn[active]
    if len (num) < 3:
        if '7' in choices:
            button (clicked, "7", posX (.4), posY (1.0), unitX (.19), unitY (.19), dark_green, green, seven)
        if '8' in choices:
            button (clicked, "8", posX (.6), posY (1.0), unitX (.19), unitY (.19), dark_green, green, eight)
        if '9' in choices:
            button (clicked, "9", posX (.8), posY (1.0), unitX (.19), unitY (.19), dark_green, green, nine)
        if '4' in choices:
            button (clicked, "4", posX (.4), posY (0.8), unitX (.19), unitY (.19), dark_green, green, four)
        if '5' in choices:
            button (clicked, "5", posX (.6), posY (0.8), unitX (.19), unitY (.19), dark_green, green, five)
        if '6' in choices:
            button (clicked, "6", posX (.8), posY (0.8), unitX (.19), unitY (.19), dark_green, green, six)
        if '1' in choices:
            button (clicked, "1", posX (.4), posY (0.6), unitX (.19), unitY (.19), dark_green, green, one)
        if '2' in choices:
            button (clicked, "2", posX (.6), posY (0.6), unitX (.19), unitY (.19), dark_green, green, two)
        if '3' in choices:
            button (clicked, "3", posX (.8), posY (0.6), unitX (.19), unitY (.19), dark_green, green, three)
        if '0' in choices:
            button (clicked, "0", posX (.4), posY (0.4), unitX (.19), unitY (.19), dark_green, green, zero)
    # button (clicked, "Enter", posX (.6), posY (0.4), unitX (.39), unitY (.19), dark_green, green, enter)
    if len (num) > 0:
        button (clicked, "Del", posX (.4), posY (0.2), unitX (.19), unitY (.19), dark_green, green, delete)

def service ():
    global menu_form, need_update
    menu_form = service_form
    need_update = True

def play (n):
    hymnexec.stop_play ()
    hymnexec.play_hymn (n)

def verse_seven ():
    play (7)

def verse_eight ():
    play (8)

def verse_nine ():
    play (9)

def verse_four ():
    play (4)

def verse_five ():
    play (5)

def verse_six ():
    play (6)

def verse_one ():
    play (1)

def verse_two ():
    play (2)

def verse_three ():
    play (3)

def verse_keypad (clicked):
    global service_choices

    if '7' in service_choices:
        button (clicked, "7", posX (.4), posY (1.0), unitX (.19), unitY (.19), dark_green, green, verse_seven)
    if '8' in service_choices:
        button (clicked, "8", posX (.6), posY (1.0), unitX (.19), unitY (.19), dark_green, green, verse_eight)
    if '9' in service_choices:
        button (clicked, "9", posX (.8), posY (1.0), unitX (.19), unitY (.19), dark_green, green, verse_nine)
    if '4' in service_choices:
        button (clicked, "4", posX (.4), posY (0.8), unitX (.19), unitY (.19), dark_green, green, verse_four)
    if '5' in service_choices:
        button (clicked, "5", posX (.6), posY (0.8), unitX (.19), unitY (.19), dark_green, green, verse_five)
    if '6' in service_choices:
        button (clicked, "6", posX (.8), posY (0.8), unitX (.19), unitY (.19), dark_green, green, verse_six)
    if '1' in service_choices:
        button (clicked, "1", posX (.4), posY (0.6), unitX (.19), unitY (.19), dark_green, green, verse_one)
    if '2' in service_choices:
        button (clicked, "2", posX (.6), posY (0.6), unitX (.19), unitY (.19), dark_green, green, verse_two)
    if '3' in service_choices:
        button (clicked, "3", posX (.8), posY (0.6), unitX (.19), unitY (.19), dark_green, green, verse_three)

def get_service_choices ():
    print "get_service_choices"
    c = []
    if active == None:
        return []
    if hymnexec.check_hymn (hymn[active]):
        v = hymnexec.max_verses (hymn[active])
        if v != 0:
            for i in range (v+1):
                c += [str (i)]
    print "get_service_choices", c
    return c

def back ():
    global menu_form
    hymnexec.stop_play ()
    menu_form = setup_form
    need_update = True

def service_menu (clicked):
    global service_choices, playing
    hymns (clicked)
    if need_update and active != None:
        service_choices = get_service_choices ()
    verse_keypad (clicked)
    button (clicked, "Stop", posX (.6), posY (0.2), unitX (.39), unitY (.19), dark_red, red, back)

def do_keys (clicked):
    if active != None:
        keypad (clicked)
        button (clicked, ">>", posX (.6), posY (0.2), unitX (.39), unitY (.19), dark_green, green, service)

def setup_menu (clicked):
    do_keys (clicked)
    hymns (clicked)

def hymns (clicked):
    hymnchoice (clicked, posX (0), posY (0.8), unitX (.3), unitY (.19), wood_dark, wood_light, 0, hymnno)
    hymnchoice (clicked, posX (0), posY (0.6), unitX (.3), unitY (.19), wood_dark, wood_light, 1, hymnno)
    hymnchoice (clicked, posX (0), posY (0.4), unitX (.3), unitY (.19), wood_dark, wood_light, 2, hymnno)

def draw_selection ():
    gameDisplay.fill (wood_dark)
    largeText = pygame.font.SysFont (None, 115)
    TextSurf, TextRect = text_objects ("Hymns", largeText, wood_light)
    TextRect.center = (posX (0.2), posY (.9))
    gameDisplay.blit (TextSurf, TextRect)

def draw_form (clicked):
    draw_selection ()
    if menu_form == setup_form:
        setup_menu (clicked)
    else:
        service_menu (clicked)
    button (clicked, "Off", posX (.0), posY (0.2), unitX (.2), unitY (.2), dark_red, red, myquit)

def select_hymns ():
    global need_update, menu_form

    menu_form = setup_form
    read_index ()
    draw_form (False)
    pygame.display.update()
    while True:
        event = pygame.event.wait ()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            myquit ()
        elif event.type == pygame.MOUSEBUTTONUP:
            need_update = True
            draw_form (True)
            if need_update:
                draw_form (False)
            pygame.display.update()
        else:
            draw_form (False)
            pygame.display.update()
        need_update = False
        # clock.tick(15)

pygame.init ()
if full_screen:
   gameDisplay = pygame.display.set_mode ((display_width, display_height), FULLSCREEN)
else:
   gameDisplay = pygame.display.set_mode ((display_width, display_height))

clock = pygame.time.Clock ()

pygame.display.set_caption ('Hymn Board')
select_hymns ()
