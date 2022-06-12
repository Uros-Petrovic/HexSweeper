class Tile:

    def __init__(self, row: int, column: int, isMine: bool, isRevealed: bool, adjacentMines: int = 0):
        self.__isMine = isMine
        self.__isRevealed = isRevealed
        self.row = row
        self.col = column
        self.adjacentMines = adjacentMines

    def __str__(self) -> str:
        return "[#]" if self.isRevealed else ("[M]" if self.isMine else f"[{self.adjacentMines}]")


    def printRevealed(self) -> str:
        return "[M]" if self.isMine() else f"[{self.adjacentMines}]"

    def drawTile(self):
        # TODO add tile drawing
        pass

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