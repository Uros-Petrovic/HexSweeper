import pygame
import os


class Tile:

    def __init__(self, isMine: bool, isRevealed: bool, xPos: int, yPos: int, adjacentMines: int = 0):
        self.__isMine = isMine
        self.__isRevealed = isRevealed
        self.adjacentMines = adjacentMines
        #self.pos = pygame.rect.Rect(xPos, yPos, 64, 64)
        self.x = xPos
        self.y = yPos
        self.surface = pygame.surface.Surface((64, 64), pygame.SRCALPHA, 32)

    def __str__(self) -> str:
        return "[#]" if self.isRevealed else ("[M]" if self.isMine else f"[{self.adjacentMines}]")


    def revealedStr(self) -> str:
        return "[M]" if self.isMine() else f"[{self.adjacentMines}]"

    def drawTile(self, window: pygame.Surface, xOff: int, yOff: int):
        
        bg = pygame.image.load(os.path.join("assets", "hexsweeper", "TileBG.png")).convert_alpha()
        font = pygame.font.Font("freesansbold.ttf", 16)
        boxStr = self.revealedStr()
        text = font.render(boxStr, True, (0, 0, 0)).convert_alpha()

        bg = pygame.transform.scale(bg, (64, 64))

        window.blit(bg, (self.x + xOff, self.y + yOff))
        window.blit(text, (self.x + xOff + 32 - font.size(boxStr)[0] / 2, self.y + yOff + 32 - font.size(boxStr)[1] / 2))


    def isRevealed(self):
        return self.__isRevealed

    def reveal(self):
        self.__isRevealed = True

    def setMine(self, isMine: bool):
        self.__isMine = isMine

    def isMine(self):
        return self.__isMine

    def getAdjacentMined(self) -> int:
        return self.adjacentMines
