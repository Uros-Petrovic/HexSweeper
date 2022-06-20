import os

import pygame

import src.hexsweeper.board as board
import src.hexsweeper.menu.menus as menus
import src.hexsweeper.tile as tile

pygame.init()

WIDTH, HEIGHT = 1440, 810
#WIDTH, HEIGHT = 720, 405
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HexSweeper")

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

FPS = 30

icon = pygame.image.load(os.path.join("assets", "hexsweeper", "1Mine.png"))
pygame.display.set_icon(icon)

def drawScreen():

    menus.activeMenu.updateScreen(WIN)

    pygame.display.update()


def main():

    #initAssets()

    menus.setMenuDims(WIDTH, HEIGHT)
    menus.activeMenu = menus.MainMenu()
    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menus.activeMenu.handleInput()

        drawScreen()
    pygame.quit()

if __name__ == '__main__':
    main()