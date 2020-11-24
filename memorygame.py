# memory game......

import random,pygame,sys
from pygame.locals import*

# variables
fps = 30
windowwidth = 800
windowheight= 600
revealspeed = 3
boxsize = 50
gapsize = 15
boardwidth = 10
boardheight = 7
assert (boardwidth * boardheight)%2==0
xmargin = int((windowwidth - (boardwidth*(boxsize+gapsize)))/2)
ymargin = int((windowheight - (boardheight*(boxsize+gapsize)))/2)
#                r   g   b
gray     =      (100,100,100)
navyblue =      ( 60, 60, 60)
white    =      (255,255,255)
red      =      (255,  0,  0)
blue     =      (  0,  0,255)
green    =      (  0,255,  0)
yellow   =      (255,255,  0)
orange   =      (255,128,  0)
purple   =      (255,  0,255)
cyan     =      (  0,255,255)
bgcolor =      navyblue
lightcolor = gray
boxcolor = white
highlightcolor = blue
donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'
allcolor = (red,green,blue,yellow,orange,purple,cyan)
allshape = (donut,square,diamond,lines,oval)
assert len(allcolor)*len(allshape)*2>=boardwidth*boardheight

def main():
    global fpsclock,displaysurf
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowwidth,windowheight))
    pygame.mixer.music.load('The Man.mp3')
    pygame.mixer.music.play(-8,0)
    mousex = 0
    mousey = 0
    pygame.display.set_caption('Memory Game')
    mainboard = getrandomizedboard()
    revealedboxes = generaterevealedboxesdata(False)
    firstselection = None
    displaysurf.fill(bgcolor)
    startgameanimation(mainboard)
   
    
    while True :
        
        
        mouseclicked = False
        displaysurf.fill(bgcolor)
        drawboard(mainboard,revealedboxes)
        for event in pygame.event.get():
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                mouseclicked = True
        boxx,boxy = getboxatpixel(mousex,mousey)
        if boxx != None and boxy != None :
            if not revealedboxes[boxx][boxy]:
                drawhighlightbox(boxx,boxy)
            if not revealedboxes[boxx][boxy] and mouseclicked:
                revealboxesanimation(mainboard,[(boxx,boxy)])
                revealedboxes[boxx][boxy] = True
                if firstselection == None:
                    firstselection =(boxx,boxy)
                else:
                    icon1shape,icon1color = getshapeandcolor(mainboard,firstselection[0],firstselection[1])
                    icon2shape,icon2color = getshapeandcolor(mainboard,boxx,boxy)

                    if icon1shape != icon2shape or icon1color !=icon2color:

                        #icons don,t match 

                        pygame.time.wait(800)
                        coverboxesanimation(mainboard,[(firstselection[0],firstselection[1]),(boxx,boxy)])
                        revealedboxes[firstselection[0]][firstselection[1]] = False
                        revealedboxes[boxx][boxy] = False

                    elif haswon(revealedboxes):
                        gamewonanimation(mainboard)
                        pygame.time.wait(2000)
                        
                        #reset the board
                        
                        mainboard = getrandomizedboard()
                        revealedboxes = generaterevealedboxesdata(False)
                        
                        #show the fully board
                        
                        drawboard(mainboard,revealedboxes)
                        pygame.dispaly.update()
                        pygame.time.wait(2000)
                        
                        #replay the start game animation
                        
                        startgameanimation(mainboard)
                        
                    firstselection = None
        
        pygame.display.update()
        fpsclock.tick(fps)

def generaterevealedboxesdata(val):
    revealedboxes = []
    for i in range(boardwidth):
        revealedboxes.append([val]*boardheight)
    return revealedboxes

def getrandomizedboard():
    #get a list of every possible shape in any color
    icons = []
    for color in allcolor:
        for shape in allshape:
            icons.append((shape,color))
    random.shuffle(icons)           #randomized the order of the icon list
    numiconused = int(boardwidth*boardheight/2)     #claculate how many icon are needed
    icons = icons[:numiconused]*2          #make two of each
    random.shuffle(icons)

    #creating the board structure
    board = []
    for x in range(boardwidth):
        column = []
        for y in range(boardheight):
            column.append(icons[0])
            del icons[0]           #remove the icons as we assign them
        board.append(column)
    return board

def lefttopcoordsofbox(boxx,boxy):
    #convert board coordinates to pixel coordinates
    left = boxx*(boxsize + gapsize)+xmargin
    top = boxy*(boxsize + gapsize)+ymargin
    return (left,top)

def getboxatpixel(x,y):
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top=lefttopcoordsofbox(boxx,boxy)
            boxRect = pygame.Rect(left, top, boxsize, boxsize)
            if boxRect.collidepoint(x,y):
                return (boxx,boxy)
    return (None,None)

def drawicon(shape,color,boxx,boxy):
    quarter = int(boxsize*0.25)
    half = int(boxsize*0.5)
    left,top=lefttopcoordsofbox(boxx,boxy)

    #draw shape
    if shape == donut:
        pygame.draw.circle(displaysurf,color,(left+half,top+half),half-5)
        pygame.draw.circle(displaysurf,bgcolor,(left+half,top+half),quarter-5)
    elif shape == square:
        pygame.draw.rect(displaysurf,color,(left+quarter,top+quarter,boxsize-half,boxsize-half))
    elif shape == diamond:
        pygame.draw.polygon(displaysurf, color, ((left + half, top), (left + boxsize- 1, top + half), (left + half, top + boxsize - 1), (left, top + half)))
    elif shape == lines:
        for i in range(0, boxsize, 4):
            pygame.draw.line(displaysurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(displaysurf, color, (left + i, top + boxsize - 1), (left + boxsize - 1, top + i))
    elif shape == oval:
        pygame.draw.ellipse(displaysurf, color, (left, top + quarter, boxsize, half))

def getshapeandcolor(board,boxx,boxy):

    return board[boxx][boxy][0],board[boxx][boxy][1]

def drawboxcovers(board,boxes,coverage):
    for box in boxes:
        left,top = lefttopcoordsofbox(box[0],box[1])
        pygame.draw.rect(displaysurf,bgcolor,(left,top,boxsize,boxsize))

        shape,color = getshapeandcolor(board,box[0],box[1])
        drawicon(shape,color,box[0],box[1])
        if coverage > 0:
            pygame.draw.rect(displaysurf,boxcolor,(left,top,coverage,boxsize))
    pygame.display.update()
    fpsclock.tick(fps)

def revealboxesanimation(board,boxestoreveal):
    for coverage in range(boxsize,(-revealspeed)-1,-revealspeed):
        drawboxcovers(board,boxestoreveal,coverage)

def coverboxesanimation(board,boxestocover):
    for coverage in range(0,boxsize+revealspeed,revealspeed):
        drawboxcovers(board,boxestocover,coverage)
        
def drawboard(board,revealed):
    #draw all the boxes in covered or revealed state
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top=lefttopcoordsofbox(boxx,boxy)
            if not revealed[boxx][boxy]:
                #draw acovered box
                pygame.draw.rect(displaysurf,boxcolor,(left,top,boxsize,boxsize))
            else :
                #draw the revealed icon
                shape,color = getshapeandcolor(board,boxx,boxy)
                drawicon(shape,color,boxx,boxy)

def drawhighlightbox(boxx,boxy):
    left,top=lefttopcoordsofbox(boxx,boxy)
    pygame.draw.rect(displaysurf,highlightcolor,(left-5,top-5,boxsize+10,4))

def startgameanimation(board):
    #random reveal boxes
    coveredboxes = generaterevealedboxesdata(False)
    boxes = []
    for x in range(boardwidth):
        for y in range(boardheight):
            boxes.append((x,y))
    drawboard(board,coveredboxes)
    revealboxesanimation(board,boxes)
    pygame.time.wait(7000)
    coverboxesanimation(board,boxes)

def gamewonanimation(board):
    #flash the bg color when player won
    coveredboxes = generaterevealedboxesdata(True)
    color1=lightcolor
    color2=bgcolor

    for i in range(13):
        color1,color2=color2,color1
        displaysurf.fill(color1)
        drawboard(board,coveredboxes)
        pygame.display.update()
        pygame.time.wait(7000)

def haswon(revealedboxes):
    for i in revealedboxes:
        if False in i :
            return False
    return True    


main()
        
    
    
        
        
                    
                
                
        
        
    
    



