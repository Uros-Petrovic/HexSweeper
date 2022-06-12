class Tile:

    def __init__(self, row: int, column: int, isMine: bool, isRevealed: bool):
        self.__isMine = isMine
        self.__isRevealed = isRevealed
        self.row = row
        self.col = column

    def drawTile(self):
        # TODO add tile drawing
        pass

    def isRevealed(self):
        return self.__isRevealed

    def reveal(self):
        self.__isRevealed = True

    def isMine(self):
        return self.__isMine

    # def matchPos(self, row: int, y: int):

    def getAdjacentMined(self, board) -> int:
        
        mineCount = 0