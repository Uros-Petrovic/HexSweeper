import pygame
import os

import src.hexsweeper.tile
import src.hexsweeper.board

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HexSweeper")

WHITE_COLOR = (255, 255, 255)

FPS = 60

icon = pygame.image.load(os.path.join("assets", "hexsweeper", "1Mine.png"))
pygame.display.set_icon(icon)

b = src.hexsweeper.board.Board(10, 10, 15)

def drawScreen():

    WIN.fill(WHITE_COLOR)
    #WIN.fill((255, 255, 0))
    b.drawBoard(WIN, 0, 0)

    pygame.display.update()


def main():

    pygame.init()
    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        drawScreen()
    pygame.quit()


def getDisplay():
    return WIN


if __name__ == '__main__':
    main()