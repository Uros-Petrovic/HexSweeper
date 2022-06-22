from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import os

import pygame
import src.hexsweeper.board as board
import src.hexsweeper.config as config
import src.hexsweeper.menu.menus as menus
from src.hexsweeper.menu.slider import Slider

from .button import Button
from .imenu import IMenu

activeMenu: IMenu = None
MENU_WIDTH: int; MENU_HEIGHT: int = None, None

def setMenuDims(width: int, height: int):
    menus.MENU_WIDTH = width
    menus.MENU_HEIGHT = height

class MainMenu(IMenu):

    MAIN_MENU_BACKGROUND = pygame.image.load(os.path.join("assets", "hexsweeper", "MainMenuBackground.png"))
    MAIN_MENU_BACKGROUND_SCALED = None

    buttonList: list = []

    def __init__(self) -> None:
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT
        buttonWidth = round(128 * (width / 1440))
        buttonHeight = round(64 * (height / 810))
        MainMenu.updateAssets(width, height)
        MainMenu.buttonList.append(Button("Start Game", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height / 2 - buttonHeight * 2, 0))
        MainMenu.buttonList.append(Button("Settings", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height / 2, 1))
        MainMenu.buttonList.append(Button("Quit", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height / 2 + buttonHeight * 2, 2))

        
        pygame.mixer.music.load(os.path.join(".", "assets", "hexsweeper", "MainMenuMusic.mp3"))
        pygame.mixer.music.play(-1)

    def drawBackground(self, window: pygame.Surface, ) -> None:
        window.blit(MainMenu.MAIN_MENU_BACKGROUND_SCALED, (0, 0))

    def handleInput(self) -> None:

        if pygame.mouse.get_pressed()[0]:

            for button in MainMenu.buttonList:

                if button.isHighlighted:
                    
                    if button.id == 0:
                        
                        self.closeMenu()
                        menus.activeMenu = GameMenu(10, 10, 25)

                    elif button.id == 1:
                        self.closeMenu()
                        menus.activeMenu = SettingsMenu()

                    elif button.id == 2:

                        pygame.quit()

    def closeMenu(self) -> None:
        MainMenu.MAIN_MENU_BACKGROUND_SCALED = None
        MainMenu.buttonList.clear()

    def updateAssets(width: int, height: int) -> None:
        MainMenu.MAIN_MENU_BACKGROUND_SCALED = pygame.transform.scale(MainMenu.MAIN_MENU_BACKGROUND, (width, height))

    def updateScreen(self, window: pygame.Surface) -> None:

        self.drawBackground(window)

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        for button in MainMenu.buttonList:
            button.isHighlighted = button.doesCollide(mouseX, mouseY)
            button.drawButton(window)


class SettingsMenu(IMenu):

    buttonList = []
    sliderList = []

    def __init__(self) -> None:
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT

        buttonWidth = round(128 * (width / 1440))
        buttonHeight = round(64 * (height / 810))

        #SettingsMenu.updateAssets(width, height)
        SettingsMenu.buttonList.append(Button("Back", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height - buttonHeight * 2, 4))

        sliderWidth = round(256 * (width / 1440))
        sliderHeight = round(64 * (height / 810))

        SettingsMenu.sliderList.append(Slider("Music {:.0%}", width / 2 - sliderWidth / 2, sliderHeight,     sliderWidth, sliderHeight, 0, 100, config.configuration.getAttribute("Music"), 0))
        SettingsMenu.sliderList.append(Slider("SFX {:.0%}",    width / 2 - sliderWidth / 2, sliderHeight * 3, sliderWidth, sliderHeight, 0, 100, config.configuration.getAttribute("Sfx"), 1))

        pygame.mixer.music.load(os.path.join("assets", "hexsweeper", "SettingsMenuMusic.mp3"))
        pygame.mixer.music.play(-1)

    def drawBackground(self, window: pygame.Surface) -> None:
        window.fill((0, 0, 0))

    def handleInput(self) -> None:      

        if pygame.mouse.get_pressed()[0]:

            for button in SettingsMenu.buttonList:

                if button.isHighlighted:

                    if button.id == 0:
                        #TODO Increase volume
                        pass

                    elif button.id == 1:
                        #TODO Decrease volume
                        pass

                    elif button.id == 2:
                        #TODO Increase SFX
                        pass

                    elif button.id == 3:
                        #TODO Decrease SFX:
                        pass

                    elif button.id == 4:
                        self.closeMenu()
                        menus.activeMenu = MainMenu()

            for slider in SettingsMenu.sliderList:

                if slider.doesCollideX(pygame.mouse.get_pos()[0]):

                    slider.updateUntilRelease()
        
        else:

            for slider in SettingsMenu.sliderList:
                slider.isHeld = False

    def closeMenu(self) -> None:
        SettingsMenu.buttonList.clear()
        SettingsMenu.sliderList.clear()



    def updateAssets(width, height) -> None:
        
        pass

    def updateScreen(self, window: pygame.Surface) -> None:
        
        self.drawBackground(window)

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        for slider in SettingsMenu.sliderList:
            slider.isHighlighted = slider.doesCollide(mouseX, mouseY)
            slider.drawSlider(window)

        for button in SettingsMenu.buttonList:
            button.isHighlighted = button.doesCollide(mouseX, mouseY)
            button.drawButton(window)

        


class GameMenu(IMenu):

    buttonList = []

    quitting: bool = None

    def __init__(self, columns: int, rows: int, mines: int) -> None:
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT
        buttonWidth = round(128 * (width / 1440))
        buttonHeight = round(64 * (height / 810))
        GameMenu.quitting = False
        GameMenu.updateAssets(width, height)
        GameMenu.buttonList.append(Button("Exit", buttonWidth, buttonHeight, 0, 0, 0))
        GameMenu.buttonList.append(Button("Cancel", buttonWidth, buttonHeight, 0, 0, 1))
        GameMenu.buttonList.append(Button("Confirm", buttonWidth, buttonHeight, 0, buttonHeight, 2))

        self.gameBoard = board.Board(columns, rows, mines, (width, height))

    def drawBackground(self, window: pygame.Surface) -> None:
        window.fill((0, 0, 0))

    def handleInput(self) -> None:

        if pygame.mouse.get_pressed()[0]:

            self.gameBoard.onMouseInput(0)

            if not GameMenu.quitting:

                for button in GameMenu.buttonList:

                    if button.isHighlighted:

                        if button.id == 0:

                            GameMenu.quitting = True

           

            elif GameMenu.quitting:

                for button in GameMenu.buttonList:

                    if button.isHighlighted:

                        if button.id == 1:
                            
                            GameMenu.quitting = False

                        elif button.id == 2:
                            
                            self.closeMenu()
                            menus.activeMenu = MainMenu()

        elif pygame.mouse.get_pressed()[2]:

            self.gameBoard.onMouseInput(1)

    def closeMenu(self) -> None:
        pass

    def updateAssets(width: int, height: int) -> None:
        pass

    def updateScreen(self, window: pygame.Surface) -> None:

        self.drawBackground(window)

        self.gameBoard.drawBoard(window, self.gameBoard.xOffset, 0)

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        if not GameMenu.quitting:

            for button in GameMenu.buttonList:

                if button.id == 0:

                    button.isHighlighted = button.doesCollide(mouseX, mouseY)
                    button.drawButton(window)

        elif GameMenu.quitting:
            
            for button in GameMenu.buttonList:

                if button.id == 1 or button.id == 2:

                        button.isHighlighted = button.doesCollide(mouseX, mouseY)
                        button.drawButton(window)
