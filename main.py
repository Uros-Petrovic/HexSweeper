import pygame
import os

import src.hexsweeper.tile as tile
import src.hexsweeper.board as board

import main

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HexSweeper")

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

FPS = 30

icon = pygame.image.load(os.path.join("assets", "hexsweeper", "1Mine.png"))
pygame.display.set_icon(icon)

b = board.Board(25, 25, 75, 0, 0)
def drawScreen():

    #WIN.fill(WHITE_COLOR)
    #WIN.fill((255, 255, 0))
    WIN.fill(BLACK_COLOR)
    b.drawBoard(WIN, 0, 0)

    pygame.display.update()


def main():

    #initAssets()

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.mouse.get_pressed()[0]:

                    b.onMouseInput(0)       

                if pygame.mouse.get_pressed()[2]:

                    b.onMouseInput(1)

        drawScreen()
    pygame.quit()


def getDisplay():
    return WIN

def initAssets():
    pass
    #tile.font = pygame.font.Font("freesansbold.ttf", 16)

if __name__ == '__main__':
    main()