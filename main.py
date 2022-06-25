import os

import pygame

import src.hexsweeper.menu.menus as menus
import src.hexsweeper.config as config

#initialize pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

#set display sizes
#WIDTH, HEIGHT = 1440, 810 #works for pc, too big for replit
#WIDTH, HEIGHT = 720, 405 #too small for pc, works for replit
WIDTH, HEIGHT = 1080, 608 #works for pc and replit
"""Menu Dimensons."""
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
"""Main Window."""
pygame.display.set_caption("HexSweeper")

#game ticks per second
FPS = 30
"""Tick Rate."""

#set the window icon for the game
icon = pygame.image.load(os.path.join("assets", "textures", "1Mine.png"))
pygame.display.set_icon(icon)

def drawScreen():
    """Method to draw the active menu, and then update the screen."""
    menus.activeMenu.updateScreen(WIN)
    pygame.display.update()


def main():
    """Main game loop."""

    #loads the HexSweeper config
    config.configuration.loadConfig()
    #specifies the menu dimensions 
    menus.setMenuDims(WIDTH, HEIGHT)
    #creates the main menu
    menus.activeMenu = menus.MainMenu()

    clock = pygame.time.Clock()
    """The main game clock."""

    #run the main game loop until the user wishes to quit
    run = True
    while run:

        #tick at the desired FPS
        clock.tick(FPS)

        #set the volume of the music based on the config value
        pygame.mixer.music.set_volume(config.configuration.getAttribute("Music") / 100)

        #loop through pygame events to handle input
        for event in pygame.event.get():
            
            #exit the main game loop if the user wishes to close the game
            if event.type == pygame.QUIT:
                run = False

            #handle mouse input if the user clicks a mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menus.activeMenu.handleInput()

        #draw the screen
        drawScreen()
    
    #close the game
    pygame.quit()

if __name__ == '__main__':
    main()