import os

import pygame

import src.hexsweeper.menu.menus as menus
import src.hexsweeper.config as config

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

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

    #pygame.mixer.Sound(os.path.join("assets", "hexsweeper", "MenuMusic.mp3")).play(-1)
    
    #initAssets()
    config.configuration.loadConfig()
    menus.setMenuDims(WIDTH, HEIGHT)
    menus.activeMenu = menus.MainMenu()
    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        pygame.mixer.music.set_volume(config.configuration.getAttribute("Music") / 100)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menus.activeMenu.handleInput()

        drawScreen()
    pygame.quit()

if __name__ == '__main__':
    main()
