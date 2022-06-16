import os

import pygame
import src.hexsweeper.board as board
import src.hexsweeper.menu.menus as menus

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

    def __init__(self) -> None:
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT
        SettingsMenu.updateAssets(width, height)
        SettingsMenu.buttonList.append(Button("Volume +", 128, 64, width / 2 - 128, height / 2 - 32 - 64, 0))
        SettingsMenu.buttonList.append(Button("Volume -", 128, 64, width / 2 + 0, height / 2 - 32 - 64, 1))
        SettingsMenu.buttonList.append(Button("SFX +", 128, 64, width / 2 - 128, height / 2 - 32 + 64, 2))
        SettingsMenu.buttonList.append(Button("SFX -", 128, 64, width / 2 + 0, height / 2 - 32 + 64, 3))
        SettingsMenu.buttonList.append(Button("Back", 128, 64, width / 2 - 64, height - 128, 4))

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

    def closeMenu(self) -> None:
        SettingsMenu.buttonList.clear()

    def updateAssets(width, height) -> None:
        #No assets
        pass

    def updateScreen(self, window: pygame.Surface) -> None:
        
        self.drawBackground(window)

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        for button in SettingsMenu.buttonList:
            button.isHighlighted = button.doesCollide(mouseX, mouseY)
            button.drawButton(window)


class GameMenu(IMenu):

    def __init__(self, columns: int, rows: int, mines: int) -> None:
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT   
        GameMenu.updateAssets(width, height)

        self.gameBoard = board.Board(columns, rows, mines)


    def drawBackground(self, window: pygame.Surface) -> None:
        window.fill((0, 0, 0))

    def handleInput(self) -> None:
        
        print(pygame.mouse.get_pressed())

        if pygame.mouse.get_pressed()[0]:

            self.gameBoard.onMouseInput(0)

        elif pygame.mouse.get_pressed()[2]:

            self.gameBoard.onMouseInput(1)

    def closeMenu(self) -> None:
        pass

    def updateAssets(width, height) -> None:
        pass

    def updateScreen(self, window: pygame.Surface) -> None:
        self.drawBackground(window)
        self.gameBoard.drawBoard(window, 0, 0)