from pickle import FALSE
import pygame
import os

FLAG_IMAGE_PATH = os.path.join("assets", "hexsweeper", "Flag.png")
UNREVEALED_TILE_IMAGE_PATH = os.path.join("assets", "hexsweeper", "TileBG.png")
UNREVEALED_HIGHLIGHT_TILE_IMAGE_PATH = os.path.join("assets", "hexsweeper", "TileBGHighlight.png")
REVEALED_TILE_IMAGE_PATH = os.path.join("assets", "hexsweeper", "RevealedTileBG.png")
REVEALED_HIGHLIGHT_TILE_IMAGE_PATH = os.path.join("assets", "hexsweeper", "RevealedTileBGHighlight.png")

TILE_NUMBER_PATHS = [

    #TODO add file paths to number images
    None,

]

class Tile:

    def __init__(self, isMine: bool, isRevealed: bool, xPos: int, yPos: int, adjacentMines: int = 0):
        self.__isMine = isMine
        self.__isRevealed = isRevealed
        self.adjacentMines = adjacentMines
        self.x = xPos
        self.y = yPos
        self.surface = pygame.surface.Surface((64, 64), pygame.SRCALPHA, 32)
        self.isHighlighted = False
        self.__isFlag = False

    def __str__(self) -> str:
        return "F" if self.isFlag() else (" " if not self.isRevealed() else ("M" if self.isMine() else f"{self.adjacentMines}"))

        """
        flag?
        revealed?
        mine?
        tiles.
        """

    def revealedStr(self) -> str:
        return "M" if self.isMine() else f"{self.adjacentMines}"

    def drawTile(self, window: pygame.Surface, xOff: int, yOff: int):
        
        bg = pygame.image.load(os.path.join("assets", "hexsweeper", "TileBGHighlight.png")).convert_alpha() if self.isHighlighted else pygame.image.load(os.path.join("assets", "hexsweeper", "TileBG.png")).convert_alpha()
        font = pygame.font.Font("freesansbold.ttf", 16)
        
        boxStr = str(self)
        text = None
        text = font.render(boxStr, True, (0, 0, 0)).convert_alpha()

        if self.isFlag():

            pass

        bg = pygame.transform.scale(bg, (64, 64))
        window.blit(bg, (self.x + xOff, self.y + yOff))
        window.blit(text, (self.x + xOff + 32 - font.size(boxStr)[0] / 2, self.y + yOff + 32 - font.size(boxStr)[1] / 2))

    def isRevealed(self):

        return self.__isRevealed

    def reveal(self):

        if self.isFlag():
            return

        self.__isRevealed = True

    def setMine(self, isMine: bool):
        self.__isMine = isMine

    def isMine(self):
        return self.__isMine

    def setFlag(self):

        if self.isRevealed():
            return

        self.__isFlag = not self.__isFlag

    def isFlag(self):

        return self.__isFlag

    def getAdjacentMines(self) -> int:
        return self.adjacentMines
