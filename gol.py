from pyclbr import Function
from random import randint
from typing import List
from xmlrpc.client import Boolean
import pygame
from copy import deepcopy


pygame.font.init()
my_font = pygame.font.SysFont('Helvetica', 30)


WIDTH, HEIGHT = 900, 500
WIN_WIDTH = WIDTH
WIN_HEIGHT = HEIGHT + 300


LEFT_SPACE = 30
CORRECT_HEIGHT = HEIGHT + 10


WIN = pygame.display.set_mode((WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Game of life")

NUM_ELEM = 100

SFONDO = (0, 0, 0)
MORTA = (20, 20, 20)
VIVA = (0, 255, 100)
WHITE = (50, 50, 50)

CELL_SIZE = 10

FPS = 60
ALIVE = 0


TITLE = my_font.render('GAME OF LIFE', False, (255, 255, 255))


# 0 MORTA
# 1 VIVA


def draw_window(mainMat: List[List], copyMat: List[List], isRunning):
    WIN.fill(SFONDO)
    ALIVES = {
        'count':0
    }
    if isRunning:
        mainMat = deepcopy(copyMat)
    else:
        ALIVES['count'] = copyMat.count(1)

    for i in range(1, len(mainMat)-1):
        for j in range(1, len(mainMat[i])-1):
            handleIteration(i, j, mainMat, copyMat, isRunning, ALIVES)
            pygame.draw.rect(WIN, WHITE, (i*CELL_SIZE, j *
                                          CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    ALIVE_TEXT = my_font.render(f'Alive: {ALIVES["count"]}', False, (154, 109, 240))

    WIN.blit(TITLE, ((WIDTH//2) - 100, CORRECT_HEIGHT - 20))
    WIN.blit(ALIVE_TEXT, (LEFT_SPACE, CORRECT_HEIGHT + 10))
    for i in range(ALIVES['count']):
        pygame.draw.rect(WIN, (154,109,245),(i * 3, CORRECT_HEIGHT+50, 3, 15))
    pygame.display.update()


def handleIteration(i, j, mainMat: List[List], copyMat: List[List], isRunning: Boolean, ALIVES):
    global ALIVE
    vive = handleCell(mainMat, i, j)
    if (mainMat[i][j] == 1):
        pygame.draw.rect(WIN, VIVA, (i*CELL_SIZE, j *
                         CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if vive != 2 and vive != 3:
            copyMat[i][j] = 0

        else:
            copyMat[i][j] = 1
            ALIVES['count'] += 1 if isRunning else 0

    else:
        pygame.draw.rect(WIN, MORTA, (i*CELL_SIZE, j *
                         CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if vive != 3:
            copyMat[i][j] = 0
        else:
            copyMat[i][j] = 1


def handleCell(mainMat: List[List], i, j):
    countVive = 0
    for k in range(i-1, i+2):
        for l in range(j-1, j+2):
            if mainMat[k][l] == 1:
                countVive += 1
    if mainMat[i][j] == 1:
        countVive -= 1

    return countVive


# For each generation of the game, a cell's status in the next generation is determined by a set of rules.
# These simple rules are as follows:
# If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
# If the cell is dead, then it springs to life only in the case that it has 3 live neighbors
# There are, of course, as many variati

def generate_random_mat():
    return [[randint(0, 1) for i in range(0, HEIGHT//CELL_SIZE)]
            for j in range(0, WIDTH//CELL_SIZE)]


def generate_empty_mat():
    return [[0 for j in range(HEIGHT//CELL_SIZE)] for i in range(WIDTH//CELL_SIZE)]


def main():
    mainMat = generate_empty_mat()
    copyMat = deepcopy(mainMat)
    run = True

    isRunning = False
    clock = pygame.time.Clock()
    draw_window(mainMat, copyMat, isRunning)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    isRunning = not isRunning
                    mainMat = deepcopy(copyMat)

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:  # 1 == left button
                    pos = pygame.mouse.get_pos()
                    # print(pos)
                    i, j = pos[0]//CELL_SIZE, pos[1]//CELL_SIZE
                    mainMat[i][j] = 1
                    
        draw_window(mainMat, copyMat, isRunning)

    pygame.quit()


if __name__ == '__main__':
    main()
