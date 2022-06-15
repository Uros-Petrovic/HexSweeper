from pprint import pprint
import pygame
import os

import src.hexsweeper.board as board
from .imenu import IMenu
import src.hexsweeper.menu.menus as menus
from .button import Button

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
        MainMenu.updateAssets(width, height)
        MainMenu.buttonList.append(Button("Start Game", 128, 64, width / 2 - 64, height / 2 - 32, 0))
        MainMenu.buttonList.append(Button("Settings", 128, 64, width / 2 - 64, height / 2 - 32 + 100, 1))
        MainMenu.buttonList.append(Button("Quit", 128, 64, width / 2 - 64, height / 2 - 32 + 200, 2))

    def drawBackground(self, window: pygame.Surface, ) -> None:
        window.blit(MainMenu.MAIN_MENU_BACKGROUND_SCALED, (0, 0))

    def handleInput(self) -> None:
        
        for button in MainMenu.buttonList:

            if button.isHighlighted:
                
                if button.id == 0:
                    
                    self.closeMenu()
                    menus.activeMenu = GameMenu()

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
                    print("XD")
                    self.closeMenu()
                    menus.activeMenu = MainMenu()

    def closeMenu(self) -> None:
        SettingsMenu.buttonList.clear()

    def updateAssets(width, height) -> None:
        pass

    def updateScreen(self, window: pygame.Surface) -> None:
        
        self.drawBackground(window)

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        for button in SettingsMenu.buttonList:
            button.isHighlighted = button.doesCollide(mouseX, mouseY)
            button.drawButton(window)


class GameMenu(IMenu):

    gameBoard: board.Board = None

    def initMenu(self) -> None:
        return super().initMenu()

    def drawBackground(self) -> None:
        return super().drawBackground()

    def handleInput(self) -> None:
        return super().handleInput()

    def drawMenu(self) -> None:
        return super().drawMenu()

    def closeMenu(self) -> None:
        return super().closeMenu()