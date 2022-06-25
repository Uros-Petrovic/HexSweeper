import os

import pygame
import src.hexsweeper.board as board
import src.hexsweeper.config as config
import src.hexsweeper.menu.menus as menus
from src.hexsweeper.menu.button import Button
from src.hexsweeper.menu.imenu import IMenu
from src.hexsweeper.menu.slider import Slider

activeMenu: IMenu = None
"""The active menu being displayed."""
MENU_WIDTH: int; MENU_HEIGHT: int = None, None
"""The dimensions of the menu."""

credits_text = [
    "Credits:",
    "",
    "   Coding      - Uros Petrovic",
    "   Game Design - Uros Petrovic",
    "   Music       - Death Rally (Not owned by me)",
    "   Game Assets - Uros Petrovic, Ryan Zhu",
    "",
    "   *Original game idea of MineSweeper is not mine",
    "",
    "   Thanks to those who helped me making this game,",
    "   I had a lot of fun making this game and I hope",
    "   that it's a good demonstration of my skills.",
]

def setMenuDims(width: int, height: int):
    """Setter for the menu dimensions."""
    menus.MENU_WIDTH = width
    menus.MENU_HEIGHT = height

class MainMenu(IMenu):
    """Class for the main menu."""

    MAIN_MENU_BACKGROUND = pygame.image.load(os.path.join("assets", "textures", "MainMenuBackground.png"))
    """Unscaled main menu background."""
    MAIN_MENU_BACKGROUND_SCALED = None
    """Scaled main menu background."""

    buttonList: list = []
    """List of buttons in this menu."""

    def __init__(self) -> None:

        #load values from the menu dimensions
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT
        buttonWidth = round(128 * (width / 1440))
        buttonHeight = round(64 * (height / 810))
        #update the assest of the main menu
        MainMenu.updateAssets(width, height)
        #append necessary buttons to the button list
        MainMenu.buttonList.append(Button("Start Game", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height / 2 - buttonHeight * 2, 0))
        MainMenu.buttonList.append(Button("Settings", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height / 2, 1))
        MainMenu.buttonList.append(Button("Quit", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height / 2 + buttonHeight * 2, 2))

        #plays the main menu music in an infinite loop
        pygame.mixer.music.load(os.path.join(".", "assets", "sounds", "MainMenuMusic.mp3"))
        pygame.mixer.music.play(-1)

    def drawBackground(self, window: pygame.Surface, ) -> None:
        #draws the scaled background image
        window.blit(MainMenu.MAIN_MENU_BACKGROUND_SCALED, (0, 0))

    def handleInput(self) -> None:

        #if the LMB is pressed
        if pygame.mouse.get_pressed()[0]:
            
            #loops through each button
            for button in MainMenu.buttonList:
                
                #checks if a button is being hovered over
                if button.isHighlighted:
                    
                    #if the button is to 'start a game'
                    if button.id == 0:
                        
                        #close the menu
                        self.closeMenu()
                        #open a new game menu
                        menus.activeMenu = GameMenu(10, 10, 20)

                    #if the button is to 'open settings'
                    elif button.id == 1:
                        #close the menu
                        self.closeMenu()
                        #open a new settings menu
                        menus.activeMenu = SettingsMenu()

                    #if the button is to 'quit'
                    elif button.id == 2:
                        
                        #close the window
                        pygame.quit()

    def closeMenu(self) -> None:
        #resets the scaled menu background image
        MainMenu.MAIN_MENU_BACKGROUND_SCALED = None
        #clears the buttonlist
        MainMenu.buttonList.clear()

    def updateAssets(width: int, height: int) -> None:
        #scales main menu background to the desired size
        MainMenu.MAIN_MENU_BACKGROUND_SCALED = pygame.transform.scale(MainMenu.MAIN_MENU_BACKGROUND, (width, height))

    def updateScreen(self, window: pygame.Surface) -> None:

        #draws the background
        self.drawBackground(window)

        #gets the position of the curosr
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        #loops through each button in the buttonlist
        for button in MainMenu.buttonList:
            #sets if the button is highlighted
            button.isHighlighted = button.doesCollide(mouseX, mouseY)
            #draws the button
            button.drawButton(window)


class SettingsMenu(IMenu):

    buttonList = []
    """List of buttons in this menu."""
    sliderList = []
    """List of sliders in this menu."""

    def __init__(self) -> None:

        #load values from the menu dimensions
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT
        buttonWidth = round(128 * (width / 1440))
        buttonHeight = round(64 * (height / 810))
        sliderWidth = round(256 * (width / 1440))
        sliderHeight = round(64 * (height / 810))

        #append necessary buttons to the button list
        SettingsMenu.buttonList.append(Button("Back", buttonWidth, buttonHeight, width / 2 - buttonWidth / 2, height - buttonHeight * 2, 0))

        #append necessary sliders to the button list
        SettingsMenu.sliderList.append(Slider("Music {:.0%}", width / 2 - sliderWidth / 2, sliderHeight,     sliderWidth, sliderHeight, 0, 100, config.configuration.getAttribute("Music"), 0))
        SettingsMenu.sliderList.append(Slider("SFX {:.0%}",    width / 2 - sliderWidth / 2, sliderHeight * 3, sliderWidth, sliderHeight, 0, 100, config.configuration.getAttribute("Sfx"), 1))

        #plays the settings menu music in an infinite loop
        pygame.mixer.music.load(os.path.join("assets", "sounds", "SettingsMenuMusic.mp3"))
        pygame.mixer.music.play(-1)

    def drawBackground(self, window: pygame.Surface) -> None:
        #fills the window with a black background
        window.fill((0, 0, 0))

    def drawCredits(self, window: pygame.Surface) -> None:
        """Draws the credits."""

        #initialized the font
        font = pygame.font.Font("freesansbold.ttf", int(menus.MENU_WIDTH / 128))

        #loops through each line in the credits
        for i, line in enumerate(menus.credits_text):
            
            #render the text
            text = font.render(line, True, (255, 255, 255))
            #draw the text in seperate lines
            window.blit(text, (0, (font.size(line)[1] + 4) * i))

    def handleInput(self) -> None: 

        #if the LMB is pressed
        if pygame.mouse.get_pressed()[0]:
            
            #loop through each button in the buttonlist
            for button in SettingsMenu.buttonList:

                #if the user is hovering over the button
                if button.isHighlighted:
                    
                    #if the button pressed is to return to the main menu
                    if button.id == 0:
                        #close the menu
                        self.closeMenu()
                        #open a new main menu
                        menus.activeMenu = MainMenu()
            
            #loop through each slider in the sliderlist
            for slider in SettingsMenu.sliderList:

                #check if the user is hovering over the slider
                if slider.doesCollideX(pygame.mouse.get_pos()[0]):

                    #update the slider until the user lets go of the LMB
                    slider.updateUntilRelease()
        
        else:

            #loop through each slider in the sliderlist
            for slider in SettingsMenu.sliderList:
                #set the isHeld of each slider to false
                slider.isHeld = False

    def closeMenu(self) -> None:
        #clears the buttonlist
        SettingsMenu.buttonList.clear()
        #clears the sliderlist
        SettingsMenu.sliderList.clear()

    def updateScreen(self, window: pygame.Surface) -> None:
        
        #draw the background
        self.drawBackground(window)
        #draw the credits
        self.drawCredits(window)

        #get the position of the cursor
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        #loop through each slider in the sliderlist
        for slider in SettingsMenu.sliderList:
            #draw the slider
            slider.drawSlider(window)

        #loop through each button in the buttonlist
        for button in SettingsMenu.buttonList:
            #change whether the button is highlighted
            button.isHighlighted = button.doesCollide(mouseX, mouseY)
            #draw the button
            button.drawButton(window)

        


class GameMenu(IMenu):

    buttonList = []
    """List of buttons in this menu."""

    quitting: bool = None
    """Whehter the user intends to quit the current game."""

    def __init__(self, columns: int, rows: int, mines: int) -> None:

        #load values from the menu dimensions
        width = menus.MENU_WIDTH
        height = menus.MENU_HEIGHT
        buttonWidth = round(128 * (width / 1440))
        buttonHeight = round(64 * (height / 810))

        GameMenu.quitting = False

        #append necessary buttons to the button list
        GameMenu.buttonList.append(Button("Exit", buttonWidth, buttonHeight, 0, 0, 0))
        GameMenu.buttonList.append(Button("Cancel", buttonWidth, buttonHeight, 0, 0, 1))
        GameMenu.buttonList.append(Button("Confirm", buttonWidth, buttonHeight, 0, buttonHeight, 2))
        
        self.gameBoard = board.Board(columns, rows, mines, (width, height))
        """Game board for this menu."""

        #plays the game menu music in an infinite loop
        pygame.mixer.music.load(os.path.join("assets", "sounds", "GameMenuMusic.mp3"))
        pygame.mixer.music.play(-1)

    def drawBackground(self, window: pygame.Surface) -> None:
        #fills the window with a black background
        window.fill((0, 0, 0))

    def handleInput(self) -> None:

        #if the LMB is pressed
        if pygame.mouse.get_pressed()[0]:
            
            #if the game is won
            if self.gameBoard.gameStatus == 1:

                #close this menu
                self.closeMenu()
                #open a new main menu
                menus.activeMenu = menus.MainMenu()
                return

            #process game board input for the LMB
            self.gameBoard.onMouseInput(0)

            #if the user does not intend to quit
            if not GameMenu.quitting:
                
                #loop through all buttons in the buttonlist
                for button in GameMenu.buttonList:

                    #if the user is hovering over that button
                    if button.isHighlighted:
                        
                        #if the button is the one that changes the intent to quit
                        if button.id == 0:
                            
                            #set the quitting intent to true
                            GameMenu.quitting = True

            elif GameMenu.quitting:
                
                #loop through all buttons in the buttonlist
                for button in GameMenu.buttonList:

                    #if the user is hovering over that button
                    if button.isHighlighted:

                        #if the button is the one that cancels the intent to quit
                        if button.id == 1:
                            
                            #set the quitting intent to false
                            GameMenu.quitting = False

                        #if the button is the one that confirms the intent to quit
                        elif button.id == 2:
                            
                            #close the menu
                            self.closeMenu()
                            #open a new main menu
                            menus.activeMenu = MainMenu()

        #if the RMB is pressed
        elif pygame.mouse.get_pressed()[2]:
            
            #process game board input for RMB
            self.gameBoard.onMouseInput(1)

    def closeMenu(self) -> None:
        #clears the buttonlist
        GameMenu.buttonList.clear()
        
    def updateScreen(self, window: pygame.Surface) -> None:
        
        #draws the background
        self.drawBackground(window)

        #if the game has been won   
        if self.gameBoard.gameStatus == True:
            #initialize variable and constants to draw the win screen
            text = "You Win!"
            extraText = f"{self.gameBoard.minesHit} Mine(s) Hit!"
            width = menus.MENU_WIDTH / 4
            height = menus.MENU_HEIGHT / 4
            xPos = menus.MENU_WIDTH / 2 - width / 2
            yPos = menus.MENU_HEIGHT / 2 - height / 2
            image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "textures", "WinButton.png")), (width, height))
            font = pygame.font.Font("freesansbold.ttf", int(height / 4))
            font2 = pygame.font.Font("freesansbold.ttf", int(height / 8))
            #draw the background image at the specified position
            window.blit(image, (xPos, yPos))
            #draw the 'You Win!' text at the specified position
            window.blit(font.render(text, True, (255, 255 ,255)), (xPos + (width / 2 - font.size(text)[0] / 2), yPos + height / 4))
            #draw the '{amount of mines hit} Mine(s) Hit!' text at the specified position
            window.blit(font2.render(extraText, True, (255, 255, 255)), (xPos + (width / 2 - font2.size(extraText)[0] / 2), yPos + height / 2))
            return
        
        #draws the game board
        self.gameBoard.drawBoard(window, self.gameBoard.xOffset, 0)

        #gets the position of the cursor
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        #if the user intends to quit
        if not GameMenu.quitting:
            
            #loop through all buttons in the buttonlist
            for button in GameMenu.buttonList:
                
                #if the button is the one that changes the intent to quit
                if button.id == 0:
                    
                    #change the highlighted status of that button
                    button.isHighlighted = button.doesCollide(mouseX, mouseY)
                    #draw that button
                    button.drawButton(window)

        #if does not the user intends to quit
        elif GameMenu.quitting:
            
            #loop through all buttons in the buttonlist
            for button in GameMenu.buttonList:

                #if the button is to confirm or cancel the intent to quit
                if button.id == 1 or button.id == 2:
                        
                        #change the highlighted status of that button
                        button.isHighlighted = button.doesCollide(mouseX, mouseY)
                        #draw that button
                        button.drawButton(window)
