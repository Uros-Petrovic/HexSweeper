import random
import math

import pygame
import src.hexsweeper.tile as tile

LEFT_MOUSE = 0
RIGHT_MOUSE = 1

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

        for col in range(columnCount):
            
            rowTiles = []

            for row in range(rowCount):

                if col % 2 == 0:

                    #rowTiles.append(tile.Tile(False, False, row * 96 + 48, col * 64 - col * 32))
                    rowTiles.append(tile.Tile(False, False, row * 64 + 32, col * 64 - col * 16))

                else:
            
                    #rowTiles.append(tile.Tile(False, False, row * 96, col * 64 - col * 32))

                    rowTiles.append(tile.Tile(False, False, row * 64, col * 64 - col * 16))

            board.append(rowTiles)

        for x in range(mineCount):
            
            while True:
                
                # -1 is included because column count is out of bounds
                mineCol = random.randint(0, columnCount - 1)
                mineRow = random.randint(0, rowCount - 1)

                if not board[mineCol][mineRow].isMine():
                    
                    board[mineCol][mineRow].setMine(True)
                    break

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


        return board
                
    def __init__(self, rows: int, columns: int, mines, xOffSet: int = 0, yOffset: int = 0) -> None:
        self.rows = rows
        self.cols = columns
        self.xOff = xOffSet
        self.yOff = yOffset
        self.board = Board.__generateBoard(rows, columns, mines)

    def drawBoard(self, window, xPos: float, yPos: float) -> None:

        near = self.getNearestBox()

        for row in self.board:

            for tile in row:
                
                tile.isHighlighted = False

                self.board[near[0]][near[1]].isHighlighted = True

                tile.drawTile(window, xPos + 1, yPos)
        

    def printBoard(self) -> None:

        for row in self.board:

            if self.board.index(row) % 2 == 0:
                print("    ",  end="")
            
            print([tile.revealedStr() for tile in row])


    def getNearestBox(self) -> tuple([int, int]):
        #(self.x + xOff + 32, self.y + yOff + 32))

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        closeCol = 0
        closeRow = 0
        closestDist = +math.inf

        for col in range(len(self.board)):
            
            for row in range(len(self.board[col])):

                tileX = self.board[col][row].x + self.xOff + 32
                tileY = self.board[col][row].y + self.yOff + 32

                distTo = math.sqrt(abs(tileX - mouseX) ** 2 + abs(tileY - mouseY) ** 2)

                if distTo < closestDist:

                    closeCol = col
                    closeRow = row
                    closestDist = distTo

        return (closeCol, closeRow)

    def onMouseInput(self, clickType: int):

        if clickType == LEFT_MOUSE:
            
            near = self.getNearestBox()
            self.board[near[0]][near[1]].reveal()

        elif clickType == RIGHT_MOUSE:

            near = self.getNearestBox()
            self.board[near[0]][near[1]].setFlag()



