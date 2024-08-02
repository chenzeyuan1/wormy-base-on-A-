
import random, pygame, sys, heapq
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
# WINDOWWIDTH = 300
# WINDOWHEIGHT = 300
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (155, 155, 155)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    # startx = random.randint(5, CELLWIDTH - 6)
    # starty = random.randint(5, CELLHEIGHT - 6)
    startx = random.randint(3, CELLWIDTH)
    starty = random.randint(3, CELLHEIGHT)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation(wormCoords)



    while True:
        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         terminate()
        #     elif event.type == KEYDOWN:
        #         if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
        #             direction = LEFT
        #         elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
        #             direction = RIGHT
        #         elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
        #             direction = UP
        #         elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
        #             direction = DOWN
        #         elif event.key == K_ESCAPE:
        #             terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            print("you hit the wall")
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                print("you hit yourself")
                return # game over

        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation(wormCoords) # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # find path to apple
        start = (wormCoords[HEAD]['x'], wormCoords[HEAD]['y'])
        end = (apple['x'], apple['y'])
        path = find_path(start, end, [(segment['x'], segment['y']) for segment in wormCoords], CELLWIDTH, CELLHEIGHT)

        if path is None:
            end = [wormCoords[-1]['x'], wormCoords[-1]['y']]
            print("no path to apple")
            path = find_path(start, end, [(segment['x'], segment['y']) for segment in wormCoords], CELLWIDTH, CELLHEIGHT)

        if path and len(path) > 1:
            next_step = path[1]
            if next_step[0] < start[0]:
                direction = LEFT
            elif next_step[0] > start[0]:
                direction = RIGHT
            elif next_step[1] < start[1]:
                direction = UP
            elif next_step[1] > start[1]:
                direction = DOWN
        
        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        # check if worm has eaten an apple
        

        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation(wormCoords):
    while True:
        temp_x = random.randint(0, CELLWIDTH - 1)
        temp_y = random.randint(0, CELLHEIGHT - 1)
        collision = False
        for segment in wormCoords:
            # print(wormCoords)
            if temp_x == segment['x'] and temp_y == segment['y']:
                collision = True
                break
        if not collision:
            return {'x': temp_x, 'y': temp_y}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

# class Node:
#     def __init__(self, position, parent=None):
#         self.position = position
#         self.parent = parent
#         self.g = 0  # 距离起点的代价
#         self.h = 0  # 距离终点的估计代价
#         self.f = 0  # 总代价

#     def __eq__(self, other):
#         return self.position == other.position

#     def __lt__(self, other):
#         return self.f < other.f

# def astar(grid, start, end):
#     open_list = []
#     closed_list = []

#     start_node = Node(start)
#     end_node = Node(end)

#     open_list.append(start_node)
#     i = 0
#     while open_list:
#         print(i)
#         i += 1
#         current_node = min(open_list, key=lambda node: node.f)
#         # current_node = open_list[0]
#         open_list.remove(current_node)
#         closed_list.append(current_node)

#         if current_node == end_node:
#             path = []
#             while current_node:
#                 path.append(current_node.position)
#                 current_node = current_node.parent
#             return path[::-1]

#         neighbors = []
#         for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
#             node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

#             if node_position[0] < 0 or node_position[0] >= len(grid) or node_position[1] < 0 or node_position[1] >= len(grid[0]):
#                 continue

#             if grid[node_position[1]][node_position[0]] != 0:
#                 continue

#             new_node = Node(node_position, current_node)
#             neighbors.append(new_node)

#         for neighbor in neighbors:
#             if neighbor in closed_list:
#                 continue

#             neighbor.g = current_node.g + 1
#             neighbor.h = abs(neighbor.position[0] - end_node.position[0]) + abs(neighbor.position[1] - end_node.position[1])
#             neighbor.f = neighbor.g + neighbor.h

#             if add_to_open(open_list, neighbor):
#                 open_list.append(neighbor)

#     return None


import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # 距离起点的代价
        self.h = 0  # 距离终点的估计代价
        self.f = 0  # 总代价

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def astar(grid, start, end):
    open_list = []
    closed_list = set()

    start_node = Node(start)
    end_node = Node(end)

    heapq.heappush(open_list, start_node)
    i = 0
    while open_list:
        # print(f"Iteration {i}: Open list size = {len(open_list)}, Closed list size = {len(closed_list)}")
        # i += 1
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        neighbors = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] < 0 or node_position[0] >= len(grid[0]) or node_position[1] < 0 or node_position[1] >= len(grid):
                continue

            if grid[node_position[1]][node_position[0]] != 0:
                # print(f"Node {node_position} is not walkable")
                continue

            new_node = Node(node_position, current_node)
            neighbors.append(new_node)

        for neighbor in neighbors:
            if neighbor.position in closed_list:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = abs(neighbor.position[0] - end_node.position[0]) + abs(neighbor.position[1] - end_node.position[1])
            neighbor.f = neighbor.g + neighbor.h

            if add_to_open(open_list, neighbor):
                heapq.heappush(open_list, neighbor)

    return None

def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.g > node.g:
            return False
    return True
def find_path(start, end, snake_body, grid_width, grid_height):
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for segment in snake_body:
        grid[segment[1]][segment[0]] = 1
        
    print_grid(grid)
    path = astar(grid, start, end)
    return path

def print_grid(grid):
    print('\n')
    # print(len(grid), len(grid[0]))
    for row in grid:
        for cell in row:
            print(cell, end=' ')
        print()  # 每一行结束后换行

if __name__ == '__main__':
    main()