import math
import random

import pygame
import src.hexsweeper.tile as tile

LEFT_MOUSE = 0
"""Constant for the LMB."""
RIGHT_MOUSE = 1
"""Constant for the RMB."""

class Board:
    """Class to create and use boards."""

    @staticmethod
    def __generateBoard(rowCount: int, columnCount: int, mineCount: int, scale: float):
        """Generates and return a board: list[][] of tiles."""

        def __checkMine(board_, col_, row_, colIncrement: int, rowIncrement: int) -> int:
            """Method to check whether a tile location is a mine."""

            #add the column to the increment
            colC = col_ + colIncrement
            rowC = row_ + rowIncrement

            #check if the indexes are greater than 0
            if colC < 0 or rowC < 0:
                return 0

            try:
                
                #returns an increment of 1 if the tile is a mine
                if board_[colC][rowC].isMine():
                    return 1

            except IndexError:
                return 0

            return 0
            
        #create an empty list
        board =  []

        #populate the empty list: board with the desired amount of rows and columns
        for col in range(columnCount):
            
            rowTiles = []

            for row in range(rowCount):

                if col % 2 == 0:

                    rowTiles.append(tile.Tile(False, False, row * scale + scale / 2, col * scale - col * scale / 4))

                else:

                    rowTiles.append(tile.Tile(False, False, row * scale, col * scale - col * scale / 4))

            board.append(rowTiles)

        #place the desired amount of mines on the board
        for x in range(mineCount):
            
            #loop until a valid spot has been selected
            while True:
                
                #generate random coordinates
                mineCol = random.randint(0, columnCount - 1)
                mineRow = random.randint(0, rowCount - 1)

                #if the spot isnt already a mine
                if not board[mineCol][mineRow].isMine():
                    
                    #set the coordinate to be a mine and break from the while loop
                    board[mineCol][mineRow].setMine(True)
                    break
        
        #get the amount of adjacent mines for each tile on the board
        for col in range(len(board)):
            
            for row in range(len(board[col])):
                
                #increment the adjacent mines counter for the tile if the specified coordinates are a mine
                board[col][row].adjacentMines += __checkMine(board, col, row, 0, -1)
                board[col][row].adjacentMines += __checkMine(board, col, row, 0, 1)
                board[col][row].adjacentMines += __checkMine(board, col, row, -1, 0)                
                board[col][row].adjacentMines += __checkMine(board, col, row, 1, 0)

                if col % 2 == 0:

                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, 1)         
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, 1)

                else:

                    board[col][row].adjacentMines += __checkMine(board, col, row, 1, -1)
                    board[col][row].adjacentMines += __checkMine(board, col, row, -1, -1)


        return board
                
    def __init__(self, columns: int, rows: int, mines: int, windowSize: tuple) -> None:
        """Board constructor."""

        self.rows = rows
        """The amount of rows in this board."""
        self.cols = columns
        """The amount of columns in this board."""

        self.scale = tile.updateAssets(columns, rows, windowSize)
        """The scale of the board."""

        self.board = Board.__generateBoard(rows, columns, mines, self.scale)
        """The list[][] of tiles on this board."""

        self.xOffset =  (windowSize[0] - (self.scale * self.rows + self.scale / 2)) / 2
        """The x offset of the board, to center it on screen."""

        self.gameStatus = False
        """The status of the game (False = ongoing; True = win)"""

        self.minesHit = 0
        """The amount of mines hit while playing on this board."""

    def drawBoard(self, window, xPos: float, yPos: float) -> None:
        """Draws all the tiles on this board."""

        #gets the nearest box to the cursor
        near = self.getNearestBox()

        #loop through each tile and 
        for row in self.board:

            for tile in row:
                
                #resets the isHighlighted value
                tile.isHighlighted = False
                
                #tries to set the nearest tile to the highlighted value
                try:

                    self.board[near[0]][near[1]].isHighlighted = True

                except TypeError:

                    pass
                
                #draws the tile
                tile.drawTile(window, xPos + 1, yPos, self.scale)
    
    def getNearestBox(self) -> tuple:
        "Gets the coordinates of the nearest box to the cursor."

        #get the mouse position
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        closeCol = 0
        """Closest column."""
        closeRow = 0
        """Closest row."""
        closestDist = +math.inf
        """Closest distance to nearest coordinate."""

        #loops through each tile in the board
        for col in range(len(self.board)):
            
            for row in range(len(self.board[col])):
                
                #gets the center of tile
                tileX = self.board[col][row].x + self.xOffset + (self.scale / 2)
                tileY = self.board[col][row].y + (self.scale / 2)

                #uses pythagorean theoreum to find the distance to the center
                distTo = math.sqrt(abs(tileX - mouseX) ** 2 + abs(tileY - mouseY) ** 2)

                #checks if the distance to the tile is less than the closest recorded distance
                if distTo < closestDist:
                    
                    #updates closest values
                    closeCol = col
                    closeRow = row
                    closestDist = distTo

        #if the cursor is within the bound of the tile
        if closestDist <= self.scale / 2: 

            #return the coordinates
            return (closeCol, closeRow)

    def onMouseInput(self, clickType: int):
        """Process mouse input on this board."""

        #if the click was a LMB
        if clickType == LEFT_MOUSE:

            def __revealZeroTiles(col, row):
                """Reveals all adjacent tiles with zero mines."""

                #if the amount of adjacent mines is zero, the tile is not a mine, and the tile is not already revealed
                if self.board[col][row].adjacentMines == 0 and not self.board[col][row].isMine() and not self.board[col][row].isRevealed():
                    
                    #reveal the passed in tile
                    self.board[col][row].reveal()

                    #loop through all the adjacant tiles 
                    for adj in self.getAdjacent(col, row):
                        
                        #reveal all the adjacent tiles with zero mines for each adjacant tile
                        __revealZeroTiles(adj[0], adj[1])
                        #reveals all adjacent tiles regardless if they have zero adjacent mines
                        self.board[adj[0]][adj[1]].reveal()
                else:
                    return          

            try:
                
                #get the nearest tile to the cursor
                near = self.getNearestBox()

                #increment the amount of mines hit only if the tile is a mine and its not revealed
                if self.board[near[0]][near[1]].isMine() and not self.board[near[0]][near[1]].isRevealed():
                    
                    self.minesHit += 1

                #reveal all adjacent tiles with zero mines
                __revealZeroTiles(near[0], near[1])

                #reveal the nearest tile regardless of the amound of adjacent mines
                self.board[near[0]][near[1]].reveal()
                
                #update win status
                self.isWin()
                    

            except TypeError:

                pass
        
        #if the click was a RMB
        elif clickType == RIGHT_MOUSE:
            
            try:
                
                #try to set the nearest box to the cursor as a flag
                near = self.getNearestBox()
                self.board[near[0]][near[1]].setFlag()

            except TypeError:
                pass

    def getAdjacent(self, col, row) -> list:
        """Get all the adjacent tiles for a specified tile."""

        def __match(matchList: list, col: int, row: int) -> list:
            """Returns a list of adjacent tiles based on the matchlist."""

            #create a temporary list
            tempList = []

            #loop through the match list
            for match in matchList:
                
                #add the increments to the indexes
                colM = col + match[0]
                rowM = row + match[1]

                #check if the indexes are greater than 0
                if colM < 0 or rowM < 0:

                    continue
                
                
                try:
                    #check if the indexes are valid
                    t = self.board[colM][rowM]
                    #append the coordinates onto the temporary list
                    tempList.append([colM, rowM])
                except IndexError:
                    continue
            
            #return the temporary list
            return tempList

        #create a list of adjacent tiles
        adjList = []

        GEN_ADJ = [
            (0, -1), (0, 1),
            (-1, 0), (1, 0),
        ]
        """Increments always adjacent."""

        EVEN_ADJ = [
            (1, 1), (-1, 1),
        ]
        """Increments increments adjacent to even column index."""

        ODD_ADJ = [
            (1, -1), (-1, -1),
        ]
        """Increments increments adjacent to odd column index."""

        #add the adjacent tiles to the adjacent list
        adjList.extend(__match(GEN_ADJ, col, row))

        #if the column is even
        if col % 2 == 0:
            
            #add the adjacent tiles to the adjacent list
            adjList.extend(__match(EVEN_ADJ, col, row))

        #if the column is odd
        else:
            
            #add the adjacent tiles to the adjacent list
            adjList.extend(__match(ODD_ADJ, col, row))

        return adjList

    def isWin(self) -> None:
        """Updates the game status."""

        #loops through each 
        for row in self.board:

            for tile_ in row:
                
                #checks if the all tiles are revealed
                if not tile_.isRevealed():
                    
                    #ensures not all mines need to be revealed
                    if not tile_.isMine():

                        return
        
        #set game status to 'win'
        self.gameStatus = True