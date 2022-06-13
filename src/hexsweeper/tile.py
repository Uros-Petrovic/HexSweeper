import pygame
import os
import src.hexsweeper.tile as tile
#initizalized in main.py$initAssets
font = None

FLAG_IMAGE_PATH = os.path.join("assets", "hexsweeper", "Flag.png")
UNREVEALED_TILE_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "TileBGNew.png"))
UNREVEALED_HIGHLIGHT_TILE_IMAGE = pygame.image.load(os.path.join("assets", "hexsweeper", "TileBGHighlight.png"))
REVEALED_TILE_IMAGE_PATH = os.path.join("assets", "hexsweeper", "RevealedTileBG.png")
REVEALED_HIGHLIGHT_TILE_IMAGE_PATH = os.path.join("assets", "hexsweeper", "RevealedTileBGHighlight.png")

#Make sure to set to none after game end
UNREVEALED_TILE_IMAGE_SCALED = None
UNREVEALED_HIGHLIGHT_TILE_IMAGE_SCALED = None

TILE_NUMBER_PATHS = [

    #TODO add file paths to number images
    None,

]

@staticmethod
def updateAssets(col, row, dims=(1000, 1000)) -> float:
    
    scale = min((dims[0] - dims[0] / row / 2) / row, dims[1] / col)

    tile.UNREVEALED_TILE_IMAGE_SCALED = pygame.transform.scale(UNREVEALED_TILE_IMAGE, (scale, scale))
    tile.UNREVEALED_HIGHLIGHT_TILE_IMAGE_SCALED = pygame.transform.scale(UNREVEALED_HIGHLIGHT_TILE_IMAGE, (scale, scale))
    tile.font = pygame.font.Font("freesansbold.ttf", int(scale / 4))

    return scale

class Tile:

    def __init__(self, isMine: bool, isRevealed: bool, xPos: int, yPos: int, adjacentMines: int = 0):
        self.__isMine = isMine
        self.__isRevealed = isRevealed
        self.adjacentMines = adjacentMines
        self.x = xPos
        self.y = yPos
        #self.surface = pygame.surface.Surface((64, 64), pygame.SRCALPHA, 32)
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

    def drawTile(self, window: pygame.Surface, xOff: int, yOff: int, scale: float):
        
        bg = UNREVEALED_HIGHLIGHT_TILE_IMAGE_SCALED.convert_alpha() if self.isHighlighted else UNREVEALED_TILE_IMAGE_SCALED.convert_alpha()
        
        boxStr = str(self)
        text = font.render(boxStr, True, (255, 255, 255)).convert_alpha()

        if self.isFlag():

            pass

        #bg = pygame.transform.scale(bg, (64, 64))

        window.blit(bg, (self.x + xOff, self.y + yOff))
        window.blit(text, (self.x + xOff + (scale / 2) - font.size(boxStr)[0] / 2, self.y + yOff + (scale / 2) - font.size(boxStr)[1] / 2))

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
