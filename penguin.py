#!/usr/bin/env python

import pygame, touchgui, isoobject
from pygame.locals import *

# display_width, display_height = 1920, 1080
display_width, display_height = 800, 600
display_width, display_height = 1920, 1080
full_screen = False
full_screen = True
isTablet, tabletOrMouse = False, None
isAudio, audio = True, None
isCombat, attackOrInteractForm, attackOrCombatForm = True, None, None
combatTestForm = None
bombButtonForm, nonCombatForm = None, None
signal_level, signal = 3, None
orig_mouse_pointer = None
current_orientation = 0
playerHealth, health, health_text = 100, None, None
playerBombs, bombs, bombcount_text = 5, None, None
playerArrows, arrows, arrowcount_text = 10, None, None
clock=pygame.time.Clock()

bombDebug, arrowDebug, healDebug, damageDebug = None, None, None, None

black = (0,0,0)
white = (255,255,255)
green = (100,200,0)
red   = (200,0,50)
blue  = (0,0,255)
yellow = (153,153,0)
orange = (204,102,0)
forest_green = (11, 102, 35)

wood_light = (166, 124, 54)
wood_dark = (76, 47, 0)

dark_red = (102, 0, 0)
dark_green = (25, 100, 50)
dark_blue = (25, 50, 150)

steel  = (128, 128, 128)
copper = (128, int (0.3 * 256.0), int (0.2 * 256.0))
gold   = (int (0.8 * 256.0), int (0.6 * 256.0), int (0.15 * 256.0))

toggle_delay = 250
    
    #
    # myquit - Exit the Program
    #

def myquit ():
    pygame.display.update ()
    pygame.time.delay (toggle_delay * 2)
    pygame.quit ()
    quit ()

    #
    # orient0, 90, 180, 270 - Orient the screen to the respective angle
    #
def orient0 ():
    isoobject.screen_orientation (0)

def orient90 ():
    isoobject.screen_orientation (90)

def orient180 ():
    isoobject.screen_orientation (180)

def orient270 ():
    isoobject.screen_orientation (270)

    #
    # orient_left - Spin the game left 90 degrees
    #

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

    #
    # orient_right - Spin the game right 90 degrees
    #

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

    #
    # orient_back - Spin the game 180 degrees
    #

def orient_back ():
    global current_orientation
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

    #
    # comat_list, image_list - Links to image locations
    #

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

    #
    # flipAudio - Disables or enables Audio
    #

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
    
    #
    # flipMouseTablet - Hide or show the cursor for mouse or tablet mode
    #

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

    #
    # interactOrAttack - Either interact, or attack with a sword
    #

def interactOrAttack ():
    global isCombat, attackOrInteractForm
    pygame.display.update()
    if isCombat:
        print("Attacking with a Sword")
    else:
        print("Interacting with X")

    #
    # arrowOrCombat - Either shoot an arrow, or switch to Combat
    #

def arrowOrCombat ():
    global isCombat, arrowOrCombatForm, attackOrInteractForm, bombButtonForm, nonCombatForm ,playerArrows, arrows
    pygame.display.update()
    if isCombat:
        if playerArrows >= 1:
            print("Shooting an Arrow")
            playerArrows = playerArrows - 1
            checkInventory()
            arrows.updateText(str(playerArrows))
        else:
            print("Out Of Arrows")
    else:
        arrowOrCombatForm.set_images(combat_list("arrowresize"))
        attackOrInteractForm.set_images(combat_list("slashresize"))
        bombButtonForm.set_images(combat_list("bombresize"))
        bombButtonForm.set_active()
        nonCombatForm.set_images(image_list("cross"))
        nonCombatForm.set_active()
        print ("Switching to Combat Menu")
        isCombat = True

    #
    # bombButton - Throw a Grenade
    #

def bombButton ():
    global isCombat, bombButtonForm, playerBombs, bombs
    pygame.display.update()
    if isCombat:
        if playerBombs >= 1: 
            print ("Placing Bomb Down")
            playerBombs = playerBombs - 1
            checkInventory()
            bombs.updateText(str(playerBombs))
        else:
            print ("Out Of Bombs")
    else:
        bombButtonForm.set_images(combat_list("blank"))
        bombButtonForm.set_frozen()

    #
    # nonCombatButton - Switch to Adventure Mode
    #
        
def nonCombatButton ():
    global isCombat, arrowOrCombatForm, attackOrInteractForm, bombButtonForm, nonCombatForm
    pygame.display.update()
    if isCombat:
        print ("Switching to Adventure Menu")
        isCombat = False
        arrowOrCombatForm.set_images(combat_list("swordresize"))
        attackOrInteractForm.set_images(image_list("buttonA"))
        bombButtonForm.set_images(combat_list("blank"))
        bombButtonForm.set_frozen()
        nonCombatForm.set_images(combat_list("blank"))
        nonCombatForm.set_frozen()
    else:
        nonCombatForm.set_images(combat_list("blank"))
        nonCombatForm.set_frozen()

    #
    # freezeButtons - Freezes unecessary buttons
    #
       
def freezeButtons():
    global health, bombs, arrows, health_text, bombcount_text, arrowcount_text
    health.set_frozen()
    health_text.set_frozen()
    bombs.set_frozen()
    bombcount_text.set_frozen()
    arrows.set_frozen()
    arrowcount_text.set_frozen()

    #
    # giveArrows - Give the player 10 arrows
    #

def giveArrows():
    global arrows, playerArrows
    print ("Giving 10 Arrows")
    playerArrows = playerArrows + 10
    checkInventory()
    arrows.updateText(str(playerArrows))

    #
    # giveBombs - Give the player 10 Grenades
    #

def giveBombs():
    global bombs, playerBombs
    print ("Giving 10 Bombs")
    playerBombs = playerBombs + 10
    checkInventory()
    bombs.updateText(str(playerBombs))

    #
    # healPlayer - Heal the Player back to 100HP
    #

def healPlayer():
    global playerHealth, health
    print ("Healing Player to Max Health")
    playerHealth = 100
    checkHealth()
    health.updateText(str(playerHealth))

    #
    # damagePlayer - Hit the player for 10HP
    #

def damagePlayer():
    global playerHealth, health
    print ("Damaging Player by 10HP")
    playerHealth = playerHealth - 10
    checkHealth()
    health.updateText(str(playerHealth))

    #
    # checkInventory - Checks the player's inventory items, and updates the colour accordingly
    #
    
def checkInventory():
    global arrows, bombs
    global playerBombs, playerArrows
    if playerArrows <= 0:
        arrows.updateColours(dark_red,dark_red,dark_red,dark_red)
    elif playerArrows > 0 and playerArrows <= 3:
        arrows.updateColours(orange,orange,orange,orange)
    elif playerArrows >= 4:
        arrows.updateColours(forest_green,forest_green,forest_green,forest_green)
    if playerBombs <= 0:
        bombs.updateColours(dark_red,dark_red,dark_red,dark_red)
    elif playerBombs > 0 and playerBombs <= 3:
        bombs.updateColours(orange,orange,orange,orange)
    elif playerBombs > 3:
        bombs.updateColours(forest_green,forest_green,forest_green,forest_green)

    #
    # checkHealth - Checks the player's health, and updates the colour accordingly
    #

def checkHealth():
    global health, playerHealth, black
    if playerHealth > 66:
        health.updateColours(forest_green,forest_green,forest_green,forest_green)
    elif playerHealth <= 66 and playerHealth > 33:
        health.updateColours(yellow,yellow,yellow,yellow)
    elif playerHealth <= 33 and playerHealth > 0:
        health.updateColours(orange,orange,orange,orange)
    elif playerHealth <= 0:
        health.updateColours(dark_red,dark_red,dark_red,dark_red)

    #
    # signal_value - Shows the current network signal strength
    #
    
def signal_value ():
    global signal
    signal.set_images (image_list ("signal3"))

def main ():
    global tabletOrMouse, audio, orig_mouse_pointer, attackOrInteractForm, arrowOrCombatForm, bombButtonForm , nonCombatForm, combatTestForm, playerHealth, playerBombs, playerArrows, signal
    global forest_green, black, dark_blue
    global health, bombs, arrows, health_text, bombcount_text, arrowcount_text
    global bombDebug, arrowDebug, healDebug, damageDebug

    pygame.init ()
    gameDisplay = pygame.display.set_mode ((display_width, display_height))

    orig_mouse_pointer = pygame.mouse.get_cursor ()

    pygame.display.set_caption ("Penguin Tower")
    touchgui.set_display (gameDisplay, display_width, display_height)
    isoobject.set_display (gameDisplay, display_width, display_height)

    # tabletOrMouse - Hides/shows the mouse cursor, used when either on PC or a Tablet
    tabletOrMouse = touchgui.image_tile (image_list ("mouse"), touchgui.posX (0.1), touchgui.posY (1.0), 100, 100, flipMouseTablet)

    # audio - Flips audio for the program
    audio = touchgui.image_tile (image_list ("audioOn"), touchgui.posX (0.0), touchgui.posY (1.0), 100, 100, flipAudio)

    # signal - displays network signal.
    signal = touchgui.image_tile (image_list ("signal1"), touchgui.posX (0.15), touchgui.posY (1.0), 100, 100, signal_value)

    # attackorInteractForm - Either attack with Sword, or interact button depending on mode
    attackOrInteractForm = touchgui.image_tile(combat_list ("slashresize"), touchgui.posX (0.95), touchgui.posY (0.1), 100, 100, interactOrAttack)
    
    # arrowOrCombatForm - Either shoot an arrow, or switch to combat mode, depending on mode
    arrowOrCombatForm = touchgui.image_tile(combat_list ("arrowresize"), touchgui.posX (0.95), touchgui.posY (0.3), 100, 100, arrowOrCombat)
    
    # bombButtonForm - Either place a grenade, or an invisible button, depending on mode
    bombButtonForm = touchgui.image_tile(combat_list ("bombresize"), touchgui.posX (0.95), touchgui.posY (0.5), 100, 100, bombButton)
    
    # nonCombatForm - Switches to adventure mode, or an invisible button, depending on mode
    nonCombatForm = touchgui.image_tile(image_list ("cross"), touchgui.posX (0.95), touchgui.posY (0.7), 100, 100, nonCombatButton)
    
    # controls - Form for our extra buttons in the top left of the screen, and the power in the top right
    controls = [touchgui.form ([touchgui.image_tile (image_list ("power"), touchgui.posX (0.95), touchgui.posY (1.0),100, 100, myquit),

                                audio,

                                touchgui.image_tile (image_list ("singleplayer"), touchgui.posX (0.05), touchgui.posY (1.0), 100, 100),

                                tabletOrMouse, signal,

                                touchgui.image_tile (image_list ("singleplayer"), touchgui.posX (0.05), touchgui.posY (1.0), 100, 100) ])]

    # movement_arrows - Form for our movement buttons on the bottom left of the screen
    movement_arrows = [touchgui.form ([touchgui.image_tile (image_list ("arrowUp"), touchgui.posX (0.05), touchgui.posY (0.30), 100, 100),

                                touchgui.image_tile (image_list ("arrowLeft"), touchgui.posX (0.00), touchgui.posY (0.20), 100, 100, orient_left),

                                touchgui.image_tile (image_list ("arrowRight"), touchgui.posX (0.10), touchgui.posY (0.20), 100, 100, orient_right),

                                touchgui.image_tile (image_list ("arrowDown"), touchgui.posX (0.05), touchgui.posY (0.10), 100, 100, orient_back)])]
    
    # health - Info panel showing off the player's HP
    health = touchgui.text_tile (forest_green, forest_green, forest_green, forest_green, str(playerHealth),touchgui.unitY (0.05), touchgui.posX (0.35), touchgui.posY (0.95), touchgui.unitX (0.045), touchgui.unitY (0.045))

    # health_text - Just a label
    health_text = touchgui.text_tile (black, black, black, black, "Health",touchgui.unitY (0.05), touchgui.posX (0.34), touchgui.posY (1.0), touchgui.unitX (0.065), touchgui.unitY (0.045))
    
    # bombs - Info panel showing off the player's grenade count
    bombs = touchgui.text_tile (forest_green, forest_green, forest_green, forest_green, str(playerBombs),touchgui.unitY (0.05), touchgui.posX (0.5), touchgui.posY (0.95), touchgui.unitX (0.045), touchgui.unitY (0.045))
    
    # bombcount_text - Just a Label
    bombcount_text = touchgui.text_tile (black, black, black, black, "Grenades",touchgui.unitY (0.05), touchgui.posX (0.475), touchgui.posY (1.0), touchgui.unitX (0.095), touchgui.unitY (0.045))

    # arrows - Info panel showing off the player's arrow count
    arrows = touchgui.text_tile (forest_green, forest_green, forest_green, forest_green, str(playerArrows),touchgui.unitY (0.05), touchgui.posX (0.65), touchgui.posY (0.95), touchgui.unitX (0.045), touchgui.unitY (0.045))

    # arrowcount_text - Just a Label
    arrowcount_text = touchgui.text_tile (black, black, black, black, "Arrows",touchgui.unitY (0.05), touchgui.posX (0.64), touchgui.posY (1.0), touchgui.unitX (0.07), touchgui.unitY (0.045))
    
    # arrowDebug - Debug button that gives the player 10 arrows
    arrowDebug = touchgui.text_tile (dark_blue, dark_blue, blue, green, "Give 10 Arrows",touchgui.unitY (0.05), touchgui.posX (0.03), touchgui.posY (0.75), touchgui.unitX (0.15), touchgui.unitY (0.045), giveArrows)
    
    # bombDebug - Debug button that gives the player 10 grenades
    bombDebug = touchgui.text_tile (dark_blue, dark_blue, blue, green, "Give 10 Grenades",touchgui.unitY (0.05), touchgui.posX (0.03), touchgui.posY (0.7), touchgui.unitX (0.17), touchgui.unitY (0.045), giveBombs)

    # healDebug - Debug button that heals the player back to 100HP
    healDebug = touchgui.text_tile (dark_blue, dark_blue, blue, green, "Heal to Full",touchgui.unitY (0.05), touchgui.posX (0.03), touchgui.posY (0.65), touchgui.unitX (0.15), touchgui.unitY (0.045), healPlayer)
    
    # damageDebug - Debug button that hits the player for 10HP
    damageDebug = touchgui.text_tile (dark_blue, dark_blue, blue, green, "10 Damage",touchgui.unitY (0.05), touchgui.posX (0.03), touchgui.posY (0.6), touchgui.unitX (0.15), touchgui.unitY (0.045), damagePlayer)
    
    # health_and_info - Form that merges the HP, Arrow and Grenade info panels and Labels
    health_and_info = [touchgui.form([ health, health_text,bombs, bombcount_text, arrows, arrowcount_text])]
    
    # interaction_buttons - Form that merges the 4 interaction buttons in the bottom right
    interaction_buttons = [touchgui.form([ attackOrInteractForm, arrowOrCombatForm, bombButtonForm ,nonCombatForm])]
    
    # debug_menu - Form that merges the debug buttons together
    debug_menu = [touchgui.form([arrowDebug, bombDebug, healDebug, damageDebug])]
    
    forms = controls + movement_arrows + interaction_buttons + health_and_info + debug_menu
    isoobject.testRoom ()                  #Renders a basic 3D room for us
    touchgui.select (forms, myquit)
    freezeButtons()
    pygame.display.update()


main ()
