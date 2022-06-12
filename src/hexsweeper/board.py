import math
import random
import src.hexsweeper.tile as tile

class Board:

    @staticmethod
    def __generateBoard(rowCount: int, columnCount: int, mineCount: int):

        def __checkMine(board_, col_, row_, colIncrement: int, rowIncrement: int) -> int:
            
            colC = col_ + colIncrement
            rowC = row_ + rowIncrement

            if colC < 0 or rowC < 0:
                return 0

            try:
                
                if board_[colC][rowC].isMine():
                    return 1

            except IndexError:
                return 0

            return 0
            

        board =  []

        for col in range(rowCount):
            
            rowTiles = []

            for row in range(columnCount):

                rowTiles.append(tile.Tile(row, col, False, False))

            board.append(rowTiles)

        for x in range(mineCount):
            
            while True:
                
                # -1 is included because column count is out of bounds
                mineCol = random.randint(0, columnCount - 1)
                mineRow = random.randint(0, rowCount - 1)

                if not board[mineCol][mineRow].isMine():
                    
                    board[mineCol][mineRow].setMine(True)
                    break
        
        board[4][0].setMine(True)

        for col in range(len(board)):
            
            for row in range(len(board[col])):

                #row -> current row
                #col -> current column

                #col, row - 1
                board[col][row].adjacentMines += __checkMine(board, col, row, 0, -1)

                #col, row + 1
                board[col][row].adjacentMines += __checkMine(board, col, row, 0, 1)
                
                if col % 2 == 0:

                    #col + 1, row
                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, 0)

                    #col + 1, row + 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, 1)         
                    
                    #col - 1, row
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, 0)
                    
                    #col + 1, row + 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, 1)

                else:
                    
                    #col + 1, row
                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, 0)

                    #col + 1, row - 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, -1)

                    #col - 1, row
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, 0)

                    #col - 1, row - 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, -1)



        for row in board:

            if board.index(row) % 2 == 0:
                print("    ",  end="")
            
            print([tile.printRevealed() for tile in row])
                
    def __init__(self, rows: int, columns: int, mines) -> None:
        self.rows = rows
        self.cols = columns
        self.board = Board.__generateBoard(rows, columns, mines)