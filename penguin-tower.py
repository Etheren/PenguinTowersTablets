#!/usr/bin/env python

import os, pygame, string, thread, sys, getopt
from pygame.locals import *
from socket import *


#
#  global variables
#
versionNumber   = 0.2
xmax            = 40    # character viewable area
ymax            = 30    # character viewable area
MaxX            = 800
MaxY            = 600
UnitX           = MaxX / xmax  # should = 20 to match png image sizes
UnitY           = MaxY / ymax  # should = 20 to match png image sizes
Resolution      = (MaxX, MaxY)
FontSize        = 24
StatusWidth     = 180
LineHeight      = 20
White           = (255, 255, 255)
Black           = (0, 0, 0)
historyList     = []    # replay list
lineNo          = 0
columnNo        = [0]
textLine        = ""
fullscreen      = 0
serverName      = "localhost"
portNumber      = 7000
debugging       = 0
programName     = "penguin-tower"
dataDirectory   = ""
soundDict       = {}
connectAttempts = 10


# a severe lack of comments (sorry)


def getFileName(subdir, filename):
    global dataDirectory

    if dataDirectory == "":
        return os.path.join(subdir, filename)
    else:
        return os.path.join(dataDirectory, os.path.join(subdir, filename))

def load_sound(name):
    class NoneSound:
        def play(self):
            pass # pass means {} in C, C++ or Java
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = getFileName('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'cannot load sound file:', fullname
        return NoneSound()
    return sound

def load_png(name):
	""" Load image and return image object"""
	fullname = getFileName('data', name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error, message:
        	print 'Cannot load image:', fullname
        	raise SystemExit, message
	return image

def initGraphics():
    global screen, font, images, background, fullscreen

    pygame.init()
    screen = pygame.display.set_mode(Resolution, fullscreen)
    pygame.display.set_caption('Penguin Tower')
    font = pygame.font.Font(None, FontSize)

    pygame.mouse.set_visible(False)
    images = {}
    for i in ['wallh', 'wallv', 'doorh', 'doorv', 'hingeh', 'hingev',
              'mann', 'mane', 'manw', 'mans',
              'manN', 'manE', 'manW', 'manS',
              'treasure',
              'arrown', 'arrows', 'arrowe', 'arroww']:
        images[i] = load_png(i + '.png')
    background = pygame.Surface(screen.get_size())

def addSound(name):
    global soundDict
    soundDict[name] = load_sound(name + ".wav")

def initSounds():
    #Load music
    addSound("arrowswish")
    addSound("brokenglass")
    addSound("fuse")
    addSound("evillaugh")
    addSound("ohno")
    addSound("ohnoexplode")
    addSound("laughexplode")
    addSound("handgrenade")
    addSound("magicarrow")
    addSound("snore")
    addSound("start")
    addSound("arrowmiss")
    addSound("brokenglass")
    addSound("applause")
    addSound("exit")

def finishGame():
    # wait 3 seconds before exiting
    pygame.time.delay(3000)
    screen = pygame.display.set_mode((640, 480))

def doHorizWall(background, x, y):
    global images

    image = images['wallh']
    imagepos = images['wallh'].get_rect()
    imagepos.top = background.get_rect().top+UnitY * y
    imagepos.left = background.get_rect().left+UnitX * x
    background.blit(image, imagepos)

def drawHorizWall(coords):
    global background
    for i in range(int(coords[0]), int(coords[2])+1):
        doHorizWall(background, i, int(coords[1]))

def doVertWall(background, x, y):
    global images

    image = images['wallv']
    imagepos = images['wallv'].get_rect()
    imagepos.top = background.get_rect().top+UnitY * y
    imagepos.left = background.get_rect().left+UnitX * x
    background.blit(image, imagepos)

def drawVertWall(coords):
    global background
    for j in range(int(coords[1]), int(coords[3])+1):
        doVertWall(background, int(coords[0]), j)

def doHorizDoor(background, x, y):
    global images

    image = images['doorh']
    imagepos = images['doorh'].get_rect()
    imagepos.top = background.get_rect().top+UnitY * y
    imagepos.left = background.get_rect().left+UnitX * x
    background.blit(image, imagepos)

def drawHorizDoor(coords):
    global background
    for i in range(int(coords[0]), int(coords[2])+1):
        doHorizDoor(background, i, int(coords[1]))

def doVertDoor(background, x, y):
    global images

    image = images['doorv']
    imagepos = images['doorv'].get_rect()
    imagepos.top = background.get_rect().top+UnitY * y
    imagepos.left = background.get_rect().left+UnitX * x
    background.blit(image, imagepos)

def drawVertDoor(coords):
    global background
    for j in range(int(coords[1]), int(coords[3])+1):
        doVertDoor(background, int(coords[0]), j)

def drawHorizHinge(coords):
    global background, images

    image = images['hingeh']
    imagepos = images['hingeh'].get_rect()
    imagepos.top = background.get_rect().top+UnitY * int(coords[1])
    imagepos.left = background.get_rect().left+UnitX * int(coords[0])
    background.blit(image, imagepos)

def drawVertHinge(coords):
    global background, images

    image = images['hingev']
    imagepos = images['hingev'].get_rect()
    imagepos.top = background.get_rect().top+UnitY * int(coords[1])
    imagepos.left = background.get_rect().left+UnitX * int(coords[0])
    background.blit(image, imagepos)

def doMan(imgname, coords):
    global background, images

    image = images[imgname]
    imagepos = images[imgname].get_rect()
    imagepos.top = background.get_rect().top+UnitY * int(coords[1])
    imagepos.left = background.get_rect().left+UnitX * int(coords[0])
    background.blit (image, imagepos)
    screen.blit (background, (0, 0))
    pygame.display.flip()

def drawMann(coords):
    doMan('mann', coords)

def drawMane(coords):
    doMan('mane', coords)

def drawMans(coords):
    doMan('mans', coords)

def drawManw(coords):
    doMan('manw', coords)

def drawManN(coords):
    doMan('manN', coords)

def drawManE(coords):
    doMan('manE', coords)

def drawManS(coords):
    doMan('manS', coords)

def drawManW(coords):
    doMan('manW', coords)

def drawTreasure(coords):
    doMan('treasure', coords)

def drawArrown(coords):
    doMan('arrown', coords)

def drawArrowe(coords):
    doMan('arrowe', coords)

def drawArrows(coords):
    doMan('arrows', coords)

def drawArroww(coords):
    doMan('arroww', coords)

def doName(font, background, name):
    text = font.render("Name " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doMap(font, background, name):
    text = font.render("Map " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*2
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doRoom(font, background, name):
    text = font.render("Room " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*3
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doWounds(font, background, name):
    text = font.render("Wounds " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*5
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doFatigue(font, background, name):
    text = font.render("Fatigue " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*6
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doMagic(font, background, name):
    text = font.render("Magic " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*8
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doArrows(font, background, name):
    text = font.render("Arrows " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*9
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doWeight(font, background, name):
    text = font.render("Weight " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*11
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doTime(font, background, name):
    text = font.render("Time " + name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*12
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doCommand(font, background, ch, desc):
    text = font.render("Command " + ch, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*14
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

    text = font.render(desc, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*15
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def drawWriteLn(name):
    global font, background, lineNo, columnNo, textLine
    text = font.render(name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*lineNo
    textpos.left = background.get_rect().left
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    lineNo = lineNo+1
    columnNo = [0]
    textLine = ""
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawWriteString(name):
    global textLine
    drawPutCh(name)
    textLine = ""

def drawPutCh(name):
    global font, background, lineNo, columnNo, textLine
    text = font.render(name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*lineNo
    textpos.left = columnNo[-1]
    textLine += name
    columnNo = columnNo + [textpos.right]
    background.blit(text, textpos)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def eraseCh():
    global font, background, lineNo, columnNo, textLine

    if len(columnNo)>0 and len(textLine)>0:
        columnNo = columnNo[:-1]
        text = font.render(textLine[-1], 1, Black)
	textLine = textLine[:-1]
        textpos = text.get_rect()
        textpos.top = background.get_rect().top+LineHeight*lineNo
        textpos.left = columnNo[-1]
        background.blit(text, textpos)
        screen.blit(background, (0, 0))
        pygame.display.flip()

def doComment1(font, background, name):
    text = font.render(name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*17
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doComment2(font, background, name):
    text = font.render(name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*18
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doComment3(font, background, name):
    text = font.render(name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*19
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doComment4(font, background, name):
    text = font.render(name, 1, White)
    textpos = text.get_rect()
    textpos.top = background.get_rect().top+LineHeight*20
    textpos.left = background.get_rect().right-StatusWidth
    blanktext = pygame.Rect(textpos.left, textpos.top,
                            StatusWidth, LineHeight)
    pygame.draw.rect(background, (0, 0, 0), blanktext)
    background.blit(text, textpos)

def doStatus(background):
    global screen, font
    # Display some text
    doName(font, background, "")
    doMap(font, background, "")
    doRoom(font, background, "")
    doFatigue(font, background, "")
    doWounds(font, background, "")
    doMagic(font, background, "")
    doArrows(font, background, "")
    doWeight(font, background, "")
    doTime(font, background, "")
    doCommand(font, background, "", "")
    doComment1(font, background, "")
    doComment2(font, background, "")
    doComment3(font, background, "")
    doComment4(font, background, "")

    # Blit everything to the screen
    screen.blit(background, (0, 0))

def doClear():
    global screen, background, lineNo
    # erase the screen
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    background.fill((0, 0, 0))
    # Blit everything to the screen
    lineNo = 0
    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # screen.blit(background, (0, 0))
    pygame.display.flip()

def drawStatus():
    global screen, background
    doStatus(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
def doSync():
    global historyList
    historyList = []

def doErase(font, background, x, y):
    blanktext = pygame.Rect(background.get_rect().left+UnitX * x,
                            background.get_rect().top+UnitY * y,
                            UnitX, UnitY)
    pygame.draw.rect(background, (0, 0, 0), blanktext)

def eraseLine(coords):
    global screen, background
    global background, images

    if len(coords) == 2:
        doErase(font, background, int(coords[0]), int(coords[1]))
    elif coords[0] == coords[2]:
        for i in range(int(coords[1]), int(coords[3])+1):
            doErase(font, background, int(coords[0]), i)
    elif coords[1] == coords[3]:
        for i in range(int(coords[0]), int(coords[2])+1):
            doErase(font, background, i, int(coords[1]))
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawCommand(font, background, ch, cmd):
    doCommand(font, background, ch, cmd)
    pygame.display.flip()

def doFlush():
    global background, screen

    screen.blit(background, (0, 0))
    pygame.display.flip()

def processLine(line):
    global font, background

    cmd = string.split(line)
    if line == 'sync':
        doSync()
    elif line == 'fl':
        doFlush()
    elif line == 'quit' or line == 'abort':
        return
    elif line == 'clear':
        doClear()
    elif line == 'status':
        drawStatus()
    elif cmd[0] == 'dWriteLn':
        drawWriteLn(line[9:])
    elif cmd[0] == 'dWriteStr':
        drawWriteString(line[10:])
    elif cmd[0] == 'dC':
        drawPutCh(cmd[1])
    elif line == 'eC':
        eraseCh()
    elif cmd[0] == 'dN':
        drawName(font, background, line[3:])
    elif cmd[0] == 'dMap':
        drawMap(font, background, line[5:])
    elif cmd[0] == 'dC1':
        drawComment1(font, background, line[4:])
    elif cmd[0] == 'dC2':
        drawComment2(font, background, line[4:])
    elif cmd[0] == 'dC3':
        drawComment3(font, background, line[4:])
    elif cmd[0] == 'dC4':
        drawComment4(font, background, line[4:])
    elif len(cmd)>1:
        if cmd[0] == 'dCMD':
            drawCommand(font, background, cmd[1], line[(len(cmd[0])+3):])
        elif cmd[0] == 'eman':
            drawMane(cmd[1:])
        elif cmd[0] == 'wman':
            drawManw(cmd[1:])
        elif cmd[0] == 'nman':
            drawMann(cmd[1:])
        elif cmd[0] == 'sman':
            drawMans(cmd[1:])
        elif cmd[0] == 'Eman':
            drawManE(cmd[1:])
        elif cmd[0] == 'Wman':
            drawManW(cmd[1:])
        elif cmd[0] == 'Nman':
            drawManN(cmd[1:])
        elif cmd[0] == 'Sman':
            drawManS(cmd[1:])
        elif cmd[0] == 'hwall':
            drawHorizWall(cmd[1:])
        elif cmd[0] == 'vwall':
            drawVertWall(cmd[1:])
        elif cmd[0] == 'hdoor':
            drawHorizDoor(cmd[1:])
        elif cmd[0] == 'vdoor':
            drawVertDoor(cmd[1:])
        elif cmd[0] == 'hhinge':
            drawHorizHinge(cmd[1:])
        elif cmd[0] == 'vhinge':
            drawVertHinge(cmd[1:])
	elif cmd[0] == 'treasure':
            drawTreasure(cmd[1:])
       	elif cmd[0] == 'war':
            drawArroww(cmd[1:])
	elif cmd[0] == 'ear':
            drawArrowe(cmd[1:])
	elif cmd[0] == 'nar':
            drawArrown(cmd[1:])
	elif cmd[0] == 'sar':
            drawArrows(cmd[1:])
        elif cmd[0] == 'dW':
            drawWounds(font, background, cmd[1])
        elif cmd[0] == 'dF':
            drawFatigue(font, background, cmd[1])
        elif cmd[0] == 'dA':
            drawArrow(font, background, cmd[1])
        elif cmd[0] == 'dM':
            drawMagic(font, background, cmd[1])
        elif cmd[0] == 'dR':
            drawRoom(font, background, cmd[1])
        elif cmd[0] == 'dw':
            drawWeight(font, background, cmd[1])
        elif cmd[0] == 'dT':
            drawTime(font, background, cmd[1])
        elif cmd[0] == 'pS':
            playSound(cmd[1])
        elif cmd[0] == 'eL':
            eraseLine(cmd[1:])
        else:
            print "Warning unknown command ", line
    else:
        print "Warning unknown command ", line

def playSound(sound):
    global soundDict
    if soundDict.has_key(sound):
       soundDict[sound].play()
    else:
       print "no sound file ", sound, " found"

def drawMap(font, background, cmd):
    doMap(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawName(font, background, cmd):
    doName(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawRoom(font, background, cmd):
    doRoom(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawWounds(font, background, cmd):
    doWounds(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawFatigue(font, background, cmd):
    doFatigue(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawArrow(font, background, cmd):
    doArrows(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawMagic(font, background, cmd):
    doMagic(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawComment1(font, background, cmd):
    doComment1(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawComment2(font, background, cmd):
    doComment2(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawComment3(font, background, cmd):
    doComment3(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawComment4(font, background, cmd):
    doComment4(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawWeight(font, background, cmd):
    doWeight(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def drawTime(font, background, cmd):
    doTime(font, background, cmd)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def stripcrlf(s):
    return s[:-1]
    
def connectServer(id, count):
    global historyList, sckt, serverName, portNumber, debugging

    # s = open('testscript', 'r')
    # line = s.readline()
    while True:
        sckt = socket(AF_INET, SOCK_STREAM)
        print "attempting to connect to %s:%d" % (serverName, portNumber)
        try:
            sckt.connect((serverName, portNumber))
            break
        except error, why:
            print "cannot find server on %s:%d" % (serverName, portNumber)
            count -= 1
            if count>0:
                print "will try again"
                portNumber += 1
            else:
                print "cannot connect to %s:%d the server is probably not running or it is not accessible" % (serverName, portNumber)
                pygame.event.post(pygame.event.Event(USEREVENT, serverLine='abort'))
                sys.exit(0)
        
    f = sckt.makefile("rb")
    line = stripcrlf(f.readline())
    while line:
        if debugging == 1:
            print line
        pygame.event.post(pygame.event.Event(USEREVENT, serverLine=line))
        pygame.time.set_timer(USEREVENT, 0)
        # pygame.time.delay(200)
        # line = s.readline()
        line = stripcrlf(f.readline())
    if debugging == 1:
        print "line =", line, " thus stopping"
    pygame.event.post(pygame.event.Event(USEREVENT, serverLine="quit"))
    pygame.time.set_timer(USEREVENT, 0)

def initEventLoop():
    global sckt, debugging

    thread.start_new(connectServer, (1, connectAttempts))
    while 1:
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                # print "key is", event.key, pygame.key.name(event.key)
                if event.key<256:
                    sckt.send(chr(event.key))
                if (event.key == K_ESCAPE):
                    screen = pygame.display.set_mode((640, 480))
                    sys.exit(0)
            elif event.type == USEREVENT:
                line = event.serverLine
                if debugging == 1:
                    print "about to process", line
                processLine(line)
                if line != 'sync':
                    historyList.append([line, pygame.time.get_ticks()])
                if line == 'quit':
                    return
                if line == 'abort':
                    sys.exit(0)


def replayHistory():
    global historyList
    lastTime = -1

    for t in historyList:
        if lastTime == -1:
           lastTime = t[1]
        else:
           pygame.time.delay(t[1]-lastTime)
           lastTime = t[1]
        processLine(t[0])

def getAnswer():
    while 1:
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_y):
                    return "y"
                elif (event.key == K_n):
                    return "n"
                if (event.key == K_ESCAPE):
                    screen = pygame.display.set_mode((640, 480))
                    sys.exit(0)

def askReplayHistory():
    global screen, font
    drawComment4(font, background, "see replay?")
    if getAnswer() == 'y':
       replayHistory()
    else:
       drawComment4(font, background, "goodbye")
       playSound('exit')

def initGameClient():
    initGraphics()
    initSounds()
    initEventLoop()
    askReplayHistory()
    finishGame()

def Usage ():
    print "%s [-vhwf] [-Idirname] fqdn:port" % programName
    print "   -v         version"
    print "   -h         help"
    print "   -w         run in full screen rather than in a %dx%d resolution window" % Resolution
    print "   -f         ditto\n"
    print "   -d         turns on debugging\n"
    print "   -Idirname  search dirname for the images and sound files\n"
    print "   default fqdn:port is %s:%s" % (serverName, portNumber)
    sys.exit(0)

def handleArgs ():
    global fullscreen, versionNumber, serverName, portNumber, debugging, dataDirectory

    try:
       optlist, list = getopt.getopt(sys.argv[1:], ':vdhwfI:')
    except getopt.GetoptError:
       Usage()
       sys.exit(0)

    for opt in optlist:
        if opt[0] == '-h':
            Usage()
        if opt[0] == '-d':
            debugging = 1
        if opt[0] == '-w' or opt[0] == '-f':
            fullscreen = FULLSCREEN
        if opt[0] == '-I':
            dataDirectory = opt[1]
        if opt[0] == '-v':
            print "morlocclient version", versionNumber
            sys.exit(0)
    if len(list)>0:
        url = string.split(list[0], ":")
        serverName = url[0]
        portNumber = int(url[1])

def main():
    handleArgs()
    initGameClient()

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
