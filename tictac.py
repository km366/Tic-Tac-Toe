import pygame
import sys
from Drawable import *
from node import Node
import random

def getResetBoxes():
    boxes = []
    y = 175
    for i in range(3):
        x = 175
        for j in range(3):
            # Box properties: filled,lowest, highest, center,current value (-1 = empty)
            boxes.append([False, (x, y), (x + 50, y + 50), (x + 25, y + 25), -1])
            x += 50
        y += 50
    return boxes

def getPositionType(index):
    if index == 4:
        return "center"
    elif index % 2 == 0:
        return "corner"
    else:
        return "edge"

    return type

def getIndexForComputerTurn():
    global move
    global leftover_boxes
    #Play a corner postion to start
    if move == 0:
        return random.choice([0, 2, 6, 8])
    node = buildTree()
    return node.getIndex()

def getMaxFromList(node):
    children = node.getChildren()
    max = children[0]
    for child in children:
        if max.getScore() < child.getScore():
            max = child
    return max

def getMinFromList(node):
    children = node.getChildren()
    min = children[0]
    for child in children:
        if min.getScore() > child.getScore():
            min = child
    return min

def getOneDGrid():
    a = []
    for i,item in enumerate(boxes):
        a.append(item[4])
    return a

def getCurrentGrid():
    current_grid=[]
    a = []
    for i,item in enumerate(boxes):
        a.append(item[4])
        if (i+1) % 3 == 0:
            current_grid.append(a)
            a=[]
    return current_grid

def checkWin(index, grid):
    if getPositionType(index)=="edge":
        if columnVictory(index,grid) or rowVictory(index,grid):
            return True
    elif getPositionType(index)=="corner":
        if index//3 == index%3:
            if columnVictory(index,grid) or rowVictory(index,grid) or leftToRightDiagonalVictory(index,grid):
                return True
        else:
            if columnVictory(index,grid) or rowVictory(index,grid) or rightToLeftDiagonalVictory(index,grid):
                return True
    else:
        if columnVictory(index, grid) or rowVictory(index, grid) or leftToRightDiagonalVictory(index,grid) or rightToLeftDiagonalVictory(index,grid):
            return True
    return False

def checkEndState(grid):
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if grid[i][j] == -1:
                return False
    return True

def clickIsOutsideGrid(pos):
    return (pos[0] < (size[0] / 2 - grid_length) or pos[0] > (size[0] / 2 + grid_length)) or (
            pos[1] < (size[1] / 2 - grid_length) or pos[1] > (size[0] / 2 + grid_length))

def leftToRightDiagonalVictory(index, current_grid):
    global win_address
    d = []
    win_address = []
    for i in range(3):
        d.append(current_grid[i][i])
        win_address.append(i*3 + i)
    if len(set(d)) == 1:
        return True
    return False

def rightToLeftDiagonalVictory(index, current_grid):
    global win_address
    c=2
    d = []
    win_address = []
    for i in range(3):
        d.append(current_grid[i][c])
        win_address.append(i*3 + c)
        c-=1
    if len(set(d)) == 1:
        return True
    return False

def columnVictory(index, current_grid):
    global win_address
    v = []
    win_address = []
    for i in range(3):
        v.append(current_grid[i][index % 3])
        win_address.append(i*3 + index % 3)
    if len(set(v)) == 1:
        return True
    return False

def rowVictory(index, current_grid):
    global win_address
    h = current_grid[index // 3]
    win_address = [x for x in range((index//3)*3, ((index//3)*3)+3)]
    if len(set(h)) == 1:
        return True
    return False

def validateUserClick(pos):
    global turn
    global move
    global leftover_boxes
    if clickIsOutsideGrid(pos):
        return
    for index, box in enumerate(boxes):
        if pos[0] in range(box[1][0], box[2][0]) and pos[1] in range(box[1][1], box[2][1]):
            if box[0]:
                return
            box[0] = True
            item = user[0]
            item.setLoc([box[3][0], box[3][1]])
            box[4] = user[1]
            leftover_boxes.remove(index)
            move += 1
            drawables.append(item)
            victoryOutput(index)
            turn = not turn
            break
    return

def normalizeGrid(grid):
    normState = [-1,-1,-1]
    print(grid)

def computerTurn():
    global turn
    global move
    global leftover_boxes
    index = getIndexForComputerTurn()
    item = comp[0]
    item.setLoc([boxes[index][3][0], boxes[index][3][1]])
    boxes[index][4] = comp[1]
    boxes[index][0] = True
    drawables.append(item)
    move += 1
    leftover_boxes.remove(index)
    victoryOutput(index)
    turn = not turn

def buildTree():
    grid = getCurrentGrid()
    n = minimax(0,comp[1], grid)
    return n

def minimax(depth, turn, grid):
    depth += 1
    node = Node(grid)
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            copyGrid = [x[:] for x in grid]
            if value == -1:
                copyGrid[i][j] = turn
                index = i*3 + j
                if checkWin(index, copyGrid):
                    child = Node(copyGrid)
                    if turn == comp[1]:
                        child.setScore(10-depth)
                    else:
                        child.setScore(depth-10)
                elif checkEndState(copyGrid):
                    child = Node(copyGrid)
                    child.setScore(0)
                else:
                    childTurn = 0 if turn == 1 else 1
                    child = minimax(depth, childTurn, copyGrid)
                child.setIndex(index)
                node.setChild(child)
    if turn == user[1]:
        n = getMinFromList(node)
    else:
        n = getMaxFromList(node)
    node.setScore(n.getScore())
    node.setIndex(n.getIndex())
    return node

def renderFonts(screen, size):
    global computerScore
    global userScore
    offset = 20
    renderScore(screen)
    title = headerFont.render('Tic-Tak-Toe', True, white)
    start_rule = font.render('X always starts first', True, white)
    options = font.render('Options:', True, white)
    quit = font.render("Press 'q' to quit", True, white)
    reset = font.render("Press 'r' to restart", True, white)
    starts = startsFont.render(("You start!" if turn else "Computer Starts!"),True, orange)
    screen.blit(title, (size[0] / 2 - title.get_rect().width / 2, offset))
    offset += 20
    screen.blit(start_rule, (size[0] / 2 - start_rule.get_rect().width / 2, offset))
    screen.blit(options, (size[0] - (options.get_rect().width + 40), offset))
    offset += 20
    screen.blit(quit, (size[0] - (quit.get_rect().width + 40), offset))
    offset += 20
    screen.blit(reset, (size[0] - (reset.get_rect().width + 40), offset))
    offset += 20
    screen.blit(starts, (size[0] / 2 - starts.get_rect().width / 2, offset))

def renderScore(screen):
    offset = 20
    score = headerFont.render('Score:', True, white)
    cScore = font.render('Computer: '+str(computerScore), True, orange)
    uScore = font.render('User: '+str(userScore), True, orange)
    screen.blit(score, (0, offset))
    screen.blit(cScore, (0, offset+20))
    screen.blit(uScore, (0, offset+40))

def makeVictoryLine(win_address):
    start_pos = boxes[win_address[0]][3]
    end_pos = boxes[win_address[2]][3]
    pygame.draw.line(screen,blue,start_pos,end_pos,6)

def victoryOutput(index):
    global turn
    global move
    global win_address
    global computerScore
    global userScore
    if move > 4:
        if checkWin(index, getCurrentGrid()):
            makeVictoryLine(win_address)
            if turn:
                userScore += 1
                endGame("You won!",screen,size)
            else:
                computerScore += 1
                endGame("Computer Won!",screen,size)
        else:
            if move == 9:
                endGame("Draw!", screen, size)


def endGame(outcome,screen, size):
    global over
    over = True
    font = pygame.font.SysFont(None, 35)
    whowon = font.render(outcome, True, orange)
    gameover = font.render('Game Over!', True, orange)
    gameover_pos = (size[0] / 2 - gameover.get_rect().width / 2, (size[0] / 2 - grid_length / 2) - gameover.get_rect().height - 15)
    whowon_pos = (size[0] / 2 - whowon.get_rect().width / 2, (size[0] / 2 + grid_length / 2) + whowon.get_rect().height + 10)
    screen.blit(gameover, gameover_pos)
    screen.blit(whowon, whowon_pos)

def resetGrid(screen, size):
    global drawables
    global boxes
    global turn
    global move
    global over
    global leftover_boxes
    global user
    global comp
    global win_address
    global playedFirst
    move = 0
    turn = random.choice([True,False])
    playedFirst = turn
    user = [Cross(0, 0), 0] if turn else [Circle(0, 0), 1]
    comp = [Circle(0, 0), 1] if turn else [Cross(0, 0), 0]
    over = False
    drawables = []
    win_address = []
    screen.fill(black)
    boxes = getResetBoxes()
    leftover_boxes = [x for x in range(9)]
    grid = Grid(grid_length)
    drawables.append(grid)
    renderFonts(screen, size)

if __name__ == '__main__':
    global computerScore
    global userScore
    computerScore = 0
    userScore = 0
    pygame.init()
    size = (500, 500)
    black = 0, 0, 0
    white = 255, 255, 255
    orange = 251, 157, 92
    blue = 93, 173, 226
    move = 0
    grid_length = 150
    headerFont = pygame.font.SysFont(None, 25)
    font = pygame.font.SysFont(None, 24)
    startsFont = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode(size)
    resetGrid(screen, size)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.__dict__['key'] == pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.__dict__['key'] == pygame.K_r:
                resetGrid(screen, size)
            if not over:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if turn:
                        validateUserClick(pos)

        for item in drawables:
            item.draw(screen, size)
            pygame.display.update()
        if not turn and not over:
            computerTurn()

        pygame.display.update()
