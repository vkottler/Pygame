import random, pygame, sys, time
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOARDWIDTH = 400
BOARDHEIGHT = 400
NUMROWS = 4
NUMCOLS = 4
bulx = 120
buly = 40

tiles = [[0, 0, 0, 0],
         [0, 2, 0, 0],
         [0, 0, 4, 0],
         [0, 0, 0, 0]]

mainBoard = pygame.Rect(bulx, buly, BOARDWIDTH, BOARDHEIGHT)
gameBlock = pygame.Rect(0, 0, BOARDWIDTH / 4 - 20, BOARDHEIGHT / 4 - 20)
random.seed()

#colors     red green blue
WHITE    = (255, 255, 255)
YELLOW   = (255, 255,   0)
DYELLOW  = (200, 255,  50)
BLACK    = (  0,   0,   0)
GRAY     = (100, 100, 100)
LIGHTGRAY= (200, 200, 200)
ORANGE   = (255, 128,   0)
DORANGE  = (255,  64,   0)
PURPLE   = (255,   0, 255)
RED      = (255,   0,   0)
BGCOLOR  = (220, 220, 220)

def main():
    global FPSCLOCK, DISPLAYSURF, fontObj
    pygame.init()
    youLose = pygame.image.load('you-lose.png')
    #soundObj = pygame.mixer.Sound('pickup.wav')
    #music = pygame.mixer.Sound('battery8bit.wav')
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Vaughn\'s 2048')
    #music.play()

    while True:
        DISPLAYSURF.fill(WHITE)
        drawBoard()
        drawTiles()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if checkLose():
            pygame.display.set_caption("You Lose")
            DISPLAYSURF.fill(WHITE)
            DISPLAYSURF.blit(youLose, (200, 100))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                #soundObj.stop()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # check key presses
                elif event.key == K_w or event.key == K_UP:
                    if checkUp():
                        #soundObj.play()
                        if not addRandomTiles():
                            #music.stop()
                            pygame.quit()
                            sys.exit()
                elif event.key == K_s or event.key == K_DOWN:
                    if checkDown():
                        #soundObj.play()
                        if not addRandomTiles():
                            #music.stop()
                            pygame.quit()
                            sys.exit()
                elif event.key == K_d or event.key == K_RIGHT:
                    if checkRight():
                        #soundObj.play()
                        if not addRandomTiles():
                            #music.stop()
                            pygame.quit()
                            sys.exit()
                elif event.key == K_a or event.key == K_LEFT:
                    if checkLeft():
                        #soundObj.play()
                        if not addRandomTiles():
                            #music.stop()
                            pygame.quit()
                            sys.exit()

def addRandomTiles():
    numToAdd = random.randint(0,10)
    if numToAdd > 8:
        numToAdd = 2
    else:
        numToAdd = 1
    valueToAdd = 0
    row = 0
    col = 0
    x = 0
    numTries = 0
    while x < numToAdd and numTries <= 64:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if tiles[col][row] == 0:
            valueToAdd = random.randint(0,10)
            if valueToAdd > 7:
                valueToAdd = 4
            else:
                valueToAdd = 2
            tiles[col][row] = valueToAdd
            x += 1
        numTries += 1
    if numTries >= 64:
        if x > 0:
            return True
        for i in range(0, 4):
            for j in range(0, 4):
                if tiles[j][i] == 0:
                    valueToAdd = random.randint(0,1)
                    if valueToAdd == 0:
                        valueToAdd = 2
                    elif valueToAdd == 1:
                        valueToAdd = 4
                    tiles[j][i] = valueToAdd
                    return True
        return False
    return True
                    
        

def drawBoard():
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, mainBoard, 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, mainBoard, 4)
    for x in range(1, 4):
        pygame.draw.line(DISPLAYSURF, BLACK, (mainBoard.left, mainBoard.top + x * (BOARDHEIGHT / 4)), (mainBoard.left + BOARDWIDTH, mainBoard.top + x * (BOARDHEIGHT / 4)), 4)
        pygame.draw.line(DISPLAYSURF, BLACK, (mainBoard.left + x * (BOARDWIDTH / 4), mainBoard.top), (mainBoard.left + x * (BOARDWIDTH / 4), mainBoard.top + BOARDHEIGHT), 4)

def drawTiles():
    currX = mainBoard.left + BOARDWIDTH / 8
    currY = mainBoard.top + BOARDHEIGHT / 8
    tempBlock = gameBlock.copy()
    tempColor = LIGHTGRAY
    text = '2'
    for i in range(0, 4):
        for j in range (0, 4):
            if tiles[j][i] != 0:
                text = str(tiles[j][i])
                tempColor = getColor(tiles[j][i])
                textSurfaceObj = fontObj.render(text, True, BLACK, tempColor)
                textRectObj = textSurfaceObj.get_rect()
                tempBlock.centerx = currX + i * BOARDWIDTH / 4
                tempBlock.centery = currY + j * BOARDHEIGHT / 4
                textRectObj = (tempBlock.centerx - textRectObj.width / 2, tempBlock.centery - textRectObj.height / 2)
                pygame.draw.rect(DISPLAYSURF, tempColor, tempBlock, 0)
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)

# for i
#   for j
#   j = row
#   i = column
#
#   Still trying to figure out why

def checkSpaceUp():
    retval = False
    for i in range(0,4): #iterate through columns
        for j in range(0, 3): #iterate through first three rows
            if (tiles[j][i] == 0): #if there is a tile that is empty
                for x in range(j, 3):
                    tiles[x][i] = tiles[x + 1][i]
                    tiles[x + 1][i] = 0
                    if (tiles[x][i] != 0 or tiles[x + 1][i] != 0):
                        retval = True
    return retval

def checkUp():
    didMove = False
    #move all tiles up through empty spaces
    #collide one tile per column if applicable
    
    while(checkSpaceUp()):
        didMove = True

    for i in range(0, 4):
        for j in range(0, 3):
            if (tiles[j][i] == tiles[j + 1][i] and tiles[j][i] != 0 and tiles[j + 1][i] != 0): #check for combine
                tiles[j][i] = 2 * tiles[j + 1][i]
                x = j + 1
                while x < 3:
                    tiles[x][i] = tiles[x + 1][i]
                    x += 1
                tiles[3][i] = 0
                didMove = True
    return didMove

def checkSpaceDown():
    retval = False
    for i in range(0,4): #iterate through columns
        j = 3
        while j > 0: #iterate through first three rows 
            if (tiles[j][i] == 0): #if there is a tile that is empty
                x = j
                while x > 0:
                    tiles[x][i] = tiles[x - 1][i]
                    tiles[x - 1][i] = 0
                    if (tiles[x][i] != 0 or tiles[x - 1][i] != 0):
                        retval = True
                    x -= 1
            j -= 1
    return retval
    

def checkDown():
    didMove = False

    while(checkSpaceDown()):
        didMove = True
    
    #check each column
    for i in range(0, 4):
        j = 3
        while j > 0:
            if (tiles[j][i] == tiles[j - 1][i] and tiles[j][i] != 0 and tiles[j - 1][i] != 0): #check for combine
                tiles[j][i] = 2 * tiles[j - 1][i]
                x = j - 1
                while x > 0:
                    tiles[x][i] = tiles[x - 1][i]
                    x -= 1
                tiles[0][i] = 0
                didMove = True
            j -= 1
    return didMove

def checkSpaceRight():
    retval = False
    i = 3
    while i > 0: #iterate through columns
        for j in range(0,4):  
            if (tiles[j][i] == 0): #if there is a tile that is empty
                x = i
                while x > 0:
                    tiles[j][x] = tiles[j][x - 1]
                    tiles[j][x - 1] = 0
                    if (tiles[j][x] != 0 or tiles[j][x - 1] != 0):
                        retval = True
                    x -= 1
        i -= 1
    return retval

def checkRight():
    didMove = False

    while(checkSpaceRight()):
        didMove = True
    
    #check each column
    i = 3
    while i > 0:
        for j in range(0, 4):
            if (tiles[j][i] == tiles[j][i - 1] and tiles[j][i] != 0 and tiles[j][i - 1] != 0): #check for combine
                tiles[j][i] = 2 * tiles[j][i - 1]
                x = i - 1
                while x > 0:
                    tiles[j][x] = tiles[j][x - 1]
                    x -= 1
                tiles[j][0] = 0
                didMove = True
        i -= 1
    return didMove

def checkSpaceLeft():
    retval = False
    for i in range(0, 3):
        for j in range(0,4):  
            if (tiles[j][i] == 0): #if there is a tile that is empty
                x = i
                while x < 3:
                    tiles[j][x] = tiles[j][x + 1]
                    tiles[j][x + 1] = 0
                    if (tiles[j][x] != 0 or tiles[j][x + 1] != 0):
                        retval = True
                    x += 1
    return retval

def checkLeft():
    didMove = False

    while(checkSpaceLeft()):
        didMove = True
    
    #check each column
    for i in range(0, 3):
        for j in range(0, 4):
            if (tiles[j][i] == tiles[j][i + 1] and tiles[j][i] != 0 and tiles[j][i + 1] != 0): #check for combine
                tiles[j][i] = 2 * tiles[j][i + 1]
                x = i + 1
                while x < 3:
                    tiles[j][x] = tiles[j][x + 1]
                    x += 1
                tiles[j][3] = 0
                didMove = True
    return didMove
    
def checkLose():
    # check if the game board is full
    for i in range(0, 4):
        for j in range(0, 4):
            if tiles[j][i] == 0:
                return False
    # check if any of the tiles could collide
    for i in range(0, 3):
        for j in range(0, 3):
            if tiles[j][i] == tiles[j + 1][i]:
                return False
            if tiles[j][i] == tiles[j][i + 1]:
                return False
    
    # check last row and last column
    for i in range(0, 3):
        if tiles[i][2] == tiles[i][3]:
            return False
    for i in range(0, 3):
        if tiles[2][i] == tiles[3][i]:
            return False
    return True

def getColor(number):
    retval = LIGHTGRAY
    if number == 4:
        retval = GRAY
    elif number == 8:
        retval = ORANGE
    elif number == 16:
        retval = DORANGE
    elif number == 32:
        retval = RED
    elif number == 64:
        retval = PURPLE
    elif number == 128:
        retval = DYELLOW
    elif number == 256:
        retval = DYELLOW
    elif number == 512:
        retval = YELLOW
    elif number == 1024:
        retval = YELLOW
    elif number == 2048:
        retval = YELLOW
    elif number == 4096:
        retval = BLACK
    return retval
    
if __name__ == '__main__':
    main()
