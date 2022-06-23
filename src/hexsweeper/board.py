import math
import random

import pygame
import src.hexsweeper.tile as tile

LEFT_MOUSE = 0
RIGHT_MOUSE = 1

class Board:

    @staticmethod
    def __generateBoard(rowCount: int, columnCount: int, mineCount: int, scale: float):

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
                    #rowTiles.append(tile.Tile(False, False, row * 64 + 32, col * 64 - col * 16))

                    rowTiles.append(tile.Tile(False, False, row * scale + scale / 2, col * scale - col * scale / 4))

                else:
            
                    #rowTiles.append(tile.Tile(False, False, row * 96, col * 64 - col * 32))
                    #rowTiles.append(tile.Tile(False, False, row * 64, col * 64 - col * 16))

                    rowTiles.append(tile.Tile(False, False, row * scale, col * scale - col * scale / 4))

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
                
                #col - 1, row
                board[col][row].adjacentMines += __checkMine(board, col, row, -1, 0)                

                #col + 1, row
                board[col][row].adjacentMines += __checkMine(board, col, row, 1, 0)

                if col % 2 == 0:

                    #col + 1, row + 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, 1)         
                    
                    #col + 1, row + 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, 1)

                else:

                    #col + 1, row - 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, -1)

                    #col - 1, row - 1
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, -1)


        return board
                
    def __init__(self, columns: int, rows: int, mines: int, windowSize: tuple([int, int])) -> None:
        self.rows = rows
        self.cols = columns
        self.scale = tile.updateAssets(columns, rows, windowSize)
        self.board = Board.__generateBoard(rows, columns, mines, self.scale)
        self.xOffset =  (windowSize[0] - (self.scale * self.rows + self.scale / 2)) / 2
        self.gameStatus = False # False = ongoing; True = win
        self.minesHit = 0

    def drawBoard(self, window, xPos: float, yPos: float) -> None:

        near = self.getNearestBox()

        for row in self.board:

            for tile in row:
                
                tile.isHighlighted = False
                
                try:

                    self.board[near[0]][near[1]].isHighlighted = True

                except TypeError:

                    pass

                tile.drawTile(window, xPos + 1, yPos, self.scale)
        

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

                tileX = self.board[col][row].x + self.xOffset + (self.scale / 2)
                tileY = self.board[col][row].y + (self.scale / 2)

                distTo = math.sqrt(abs(tileX - mouseX) ** 2 + abs(tileY - mouseY) ** 2)

                if distTo < closestDist:

                    closeCol = col
                    closeRow = row
                    closestDist = distTo

        if closestDist <= self.scale / 2: 

            return (closeCol, closeRow)

    def onMouseInput(self, clickType: int):

        if clickType == LEFT_MOUSE:
            
            def __revealZeroTiles(col, row):

                if self.board[col][row].adjacentMines == 0 and not self.board[col][row].isMine() and not self.board[col][row].isRevealed():
                    
                    self.board[col][row].reveal()

                    for adj in self.getAdjacent(col, row):
                
                        __revealZeroTiles(adj[0], adj[1])
                        self.board[adj[0]][adj[1]].reveal()
                else:
                    return          

            try:

                near = self.getNearestBox()

                __revealZeroTiles(near[0], near[1])

                if self.board[near[0]][near[1]].isMine():
                    
                    self.minesHit += 1

                self.board[near[0]][near[1]].reveal()
                
                self.isWin()
                    

            except TypeError:

                pass

        elif clickType == RIGHT_MOUSE:
            
            try:

                near = self.getNearestBox()
                self.board[near[0]][near[1]].setFlag()

            except TypeError:

                pass

    def getAdjacent(self, col, row) -> list:

        def __match(matchList: list, col: int, row: int) -> list:

            tempList = []

            for match in matchList:
            
                colM = col + match[0]
                rowM = row + match[1]

                if colM < 0 or rowM < 0:

                    continue

                try:
                    t = self.board[colM][rowM]
                    tempList.append([colM, rowM])
                except IndexError:
                    continue
                
            return tempList

        adjList = []

        GEN_ADJ = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]

        EVEN_ADJ = [
            (1, 1),
            (-1, 1),
        ]

        ODD_ADJ = [
            (1, -1),
            (-1, -1),
        ]

        adjList.extend(__match(GEN_ADJ, col, row))

        if col % 2 == 0:

            adjList.extend(__match(EVEN_ADJ, col, row))

        else:

            adjList.extend(__match(ODD_ADJ, col, row))

        return adjList

    def isWin(self) -> None:

        for row in self.board:

            for tile_ in row:

                if not tile_.isRevealed():
                    
                    if not tile_.isMine():

                        return
        
        self.gameStatus = True
