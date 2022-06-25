import pygame
import os
import src.hexsweeper.tile as tile
import src.hexsweeper.config as config

FLAG_IMAGE = pygame.image.load(os.path.join("assets", "textures", "Flag.png"))
"""Flag image."""
MINE_IMAGE = pygame.image.load(os.path.join("assets", "textures", "Mine.png"))
"""Mine image."""
REVEALED_TILE_IMAGE = pygame.image.load(os.path.join("assets", "textures", "TileBackgroundRevealed.png"))
"""Revealed tile image."""
UNREVEALED_TILE_IMAGE = pygame.image.load(os.path.join("assets", "textures", "TileBackground.png"))
"""Unreavealed tile image."""
HIGHLIGHT_TILE_IMAGE = pygame.image.load(os.path.join("assets", "textures", "TileBackgroundHighlight.png"))
"""Highlighted tile image."""

FLAG_IMAGE_SCALED = None
"""Scaled flag image."""
MINE_IMAGE_SCALED = None
"""Scaled mine image."""
REVEALED_TILE_IMAGE_SCALED = None
"""Scaled revealed tile image."""
UNREVEALED_TILE_IMAGE_SCALED = None
"""Scaled unrevealed tile image."""
HIGHLIGHT_TILE_IMAGE_SCALED = None
"""Scaled highlighted tile image."""

TILE_NUMBER_COLORS = [

    0xFFFFFFFF,
    0x2090ffFF,
    0x4cbe51FF,
    0xff3b3bFF,
    0xff35eeFF,
    0xffca18FF,
    0x00f2feFF,

]
"""Adjacent mine colors.
"""
def updateAssets(col, row, dims=(1000, 1000)) -> float:
    """Updates the scaled images and sets the designated size font."""

    #determins the a valid scale for the specified dimensions
    scale = min((dims[0] - dims[0] / row / 2) / row, dims[1] / col)

    #scales the images to the designated size and sets the font
    tile.UNREVEALED_TILE_IMAGE_SCALED = pygame.transform.scale(UNREVEALED_TILE_IMAGE, (scale, scale))
    tile.HIGHLIGHT_TILE_IMAGE_SCALED = pygame.transform.scale(HIGHLIGHT_TILE_IMAGE, (scale, scale))
    tile.REVEALED_TILE_IMAGE_SCALED = pygame.transform.scale(REVEALED_TILE_IMAGE, (scale, scale))
    tile.MINE_IMAGE_SCALED = pygame.transform.scale(MINE_IMAGE, (scale / 2, scale / 2))
    tile.FLAG_IMAGE_SCALED = pygame.transform.scale(FLAG_IMAGE, (scale / 2, scale / 2))
    tile.font = pygame.font.Font("freesansbold.ttf", int(scale / 4))

    return scale

class Tile:
    """Class to hold all the values of a tile."""

    def __init__(self, isMine: bool, isRevealed: bool, xPos: int, yPos: int, adjacentMines: int = 0):
        "Tile constructor."
        
        self.x = xPos
        """The x position of this tile."""
        self.y = yPos
        """The y position of this tile."""

        self.__isMine = isMine
        """Whether this tile is a mine."""

        self.__isRevealed = isRevealed
        """Whether this tile is revealed."""

        self.adjacentMines = adjacentMines
        """The amount of adjacent mines."""

        self.isHighlighted = False
        """Whether the user is hovering over this tile."""

        self.__isFlag = False
        """Whether this tile has a flag placed on it."""

    def __str__(self) -> str:
        """Returns the state of this tile as a string."""
        return "F" if self.isFlag() else (" " if not self.isRevealed() else ("M" if self.isMine() else f"{self.adjacentMines}"))

    def revealedStr(self) -> str:
        """Returns the revealed state of this mine."""
        return "M" if self.isMine() else f"{self.adjacentMines}"

    def drawTile(self, window: pygame.Surface, xOff: int, yOff: int, scale: float):
        """Draws this tile on the specified window."""

        #initializes the background and foreground variables of this tile
        background: pygame.Surface = None
        foreground: pygame.Surface = None

        #set the background
        #if the tile is being hovered over
        if self.isHighlighted:
            
            background = HIGHLIGHT_TILE_IMAGE_SCALED.convert_alpha()
        
        #if the tile is not being hovered over
        else:
            
            #if the tile is revealed
            if self.isRevealed():
                
                background = REVEALED_TILE_IMAGE_SCALED.convert_alpha()

            #if the tile is not revealed   
            else:

                background = UNREVEALED_TILE_IMAGE_SCALED.convert_alpha()
                    
        #set the foreground
        #if the tile is flagged
        if self.isFlag():

            foreground = FLAG_IMAGE_SCALED
        
        #if the tile isnt revealed or the tile is not a mine and has no adjacent mines
        elif not self.isRevealed() or (self.adjacentMines == 0 and not self.isMine()):

            #foreground is not drawn
            foreground = tile.font.render("", True, tile.TILE_NUMBER_COLORS[self.adjacentMines]).convert_alpha()

        #if the tile is revealed and the tile is a mine
        elif self.isRevealed() and self.isMine():

            foreground = MINE_IMAGE_SCALED
        
        #otherwise, draw the colored string (number of adjacent mines)
        else:

            foreground = tile.font.render(str(self.adjacentMines), True, tile.TILE_NUMBER_COLORS[self.adjacentMines]).convert_alpha()

        #draw the background and foreground at the specified locations
        window.blit(background, (self.x + xOff, self.y + yOff))
        window.blit(foreground, (self.x + xOff + (scale / 2) - foreground.get_size()[0] / 2, self.y + yOff + (scale / 2) - foreground.get_size()[1] / 2))

    def isRevealed(self):
        """Getter for whether this tile is revealed."""
        return self.__isRevealed

    def reveal(self):
        """Reveals this tile."""

        if self.isFlag():
            return

        self.__isRevealed = True

    def setMine(self, isMine: bool):
        """Setter for whether this tile is a mine."""
        self.__isMine = isMine

    def isMine(self):
        """Getter for whether this tile is a mine."""
        return self.__isMine

    def setFlag(self):
        """Setter for whether this tile is flagged."""
        if self.isRevealed():
            return

        self.__isFlag = not self.__isFlag

    def isFlag(self):
        """Getter for whether this tile is flagged."""
        return self.__isFlag

    def getAdjacentMines(self) -> int:
        """Getter for the amount of mines adjacent to this tile."""
        return self.adjacentMines
        