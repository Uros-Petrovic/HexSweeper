class Board:

    @staticmethod
    def __generateBoard(rowCount: int, columnCount: int, mineCount: int):

        for x in range(mineCount):
            pass


    def __init__(self, rows: int, columns: int, mines) -> None:
        self.rows = rows
        self.cols = columns
        self.boardd = Board.__generateBoard(rows, columns, mines)