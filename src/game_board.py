import random
class Board:
    def __init__(self, copy = False, board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], empty_tiles = set()):
        self._copy = copy
        self._end_game = False
        self._random_list = [2]*9 + [4]
        self._score = 0
        self._weight = [[pow(4,3),pow(4,2),pow(4,1),pow(4,4)],[pow(4,4),pow(4,5),pow(4,6),pow(4,7)],[pow(4,11),pow(4,10),pow(4,9),pow(4,8)],[pow(4,12),pow(4,13),pow(4,14),pow(4,15)]]
        self._board = board
        self._empty_tiles = empty_tiles
        if not copy:
            for i in range (4):
                for j in range(4):
                    self._empty_tiles.add((i,j))
            self.init_board()
            

    def init_board(self):
        row,col = random.choice(list(self._empty_tiles))
        value = random.choice(self._random_list)
        self._board[row][col] = value
        self._empty_tiles.remove((row,col))

    def board(self):
        return self._board
    def empty_tiles(self):
        return self._empty_tiles
#function to move all tiles of a column or row to a certain direction
    def switch(self,pos: tuple, move: int, direction: str):
        x,y = pos[0], pos[1]
        if direction == "left":
            start = y-move
            for i in range(start,4):
                if i >= 4-move:
                    self._board[x][i] = 0
                    self._empty_tiles.add((x,i))
                else:
                    self._board[x][i] = self._board[x][i+move]
                if (x,i) not in self._empty_tiles and self._board[x][i] == 0:
                    self._empty_tiles.add((x,i))
                elif (x,i) in self._empty_tiles and self._board[x][i] != 0:
                    self._empty_tiles.remove((x,i))
        elif direction == "right":
            start = y + move
            for i in range(start,-1,-1):
                if i < move:
                    self._board[x][i] = 0
                else:
                    self._board[x][i] = self._board[x][i-move]
                if (x,i) not in self._empty_tiles and self._board[x][i] == 0:
                    self._empty_tiles.add((x,i))
                elif (x,i) in self._empty_tiles and self._board[x][i] != 0:
                    self._empty_tiles.remove((x,i))
        elif direction == "up":
            start = x-move
            for i in range(start,4):
                if i >= 4-move:
                    self._board[i][y] = 0
                else:
                    self._board[i][y] = self._board[i+move][y]
                if (i,y) not in self._empty_tiles and self._board[i][y] == 0:
                    self._empty_tiles.add((i,y))
                elif (x,i) in self._empty_tiles and self._board[i][y] != 0:
                    self._empty_tiles.remove((i,y))
        elif direction == "down":
            start = x + move
            for i in range(start,-1,-1):
                if i < move:
                    self._board[i][y] = 0
                else:
                    self._board[i][y] = self._board[i-move][y]
                if (i,y) not in self._empty_tiles and self._board[i][y] == 0:
                    self._empty_tiles.add((i,y))
                elif (i,y) in self._empty_tiles and self._board[i][y] != 0:
                    self._empty_tiles.remove((i,y))

    def merged(self,pos,direction):
        x,y = pos[0], pos[1]
        if direction == "left" and y > 0 and self._board[x][y] == self._board[x][y-1]:
            self._board[x][y-1] *= 2
            self._score += self._board[x][y-1]
            self.switch((x,y+1),1,direction)
            return True
        if direction == "right" and y < 3 and self._board[x][y] == self._board[x][y+1]:
            self._board[x][y+1] *= 2
            self._score += self._board[x][y+1]
            self.switch((x,y-1),1,direction)
            return True
        if direction == "up" and x > 0 and self._board[x][y] == self._board[x-1][y]:
            self._board[x-1][y] *= 2
            self._score += self._board[x-1][y]
            self.switch((x+1,y),1,direction)
            return True
        if direction == "down" and x < 3 and self._board[x][y] == self._board[x+1][y]:
            self._board[x+1][y] *= 2
            self._score += self._board[x+1][y]
            self.switch((x-1,y),1,direction)
            return True
        
    def check_empty_tiles(self,pos):
        return pos in self._empty_tiles    

    def move_left(self):
        for i in range(4):
            row = self._board[i]
            zeros = 0
            j = 0
            while j <= 3:
                #keep track of the number of zero tiles
                if row[j] == 0:
                    zeros += 1
                    j += 1
                    continue
                #start moving tiles to the chosen direction when reaching a non-zero tile
                if zeros > 0:
                    self.switch((i,j),zeros,"left")
                    j = 0
                    zeros = 0
                    continue
                #check if the current tile can be merged with the tile on its left side, if yes, then merge
                if self.merged((i,j),"left"):
                    break
                j += 1
        if not self._copy:
            row,col = random.choice(list(self._empty_tiles))
            value = random.choice(self._random_list)
            self._board[row][col] = value
            self._empty_tiles.remove((row,col))
            if self.no_empty_tiles():
                self._end_game = True
                return f"Game over! Best score: {self._score}"
            else:
                return self.__str__()
        

    def move_right(self):
        for i in range(4):
            row = self._board[i]
            zeros = 0
            j = 3
            #loof through the row from right to left and stop when it reaches the leftmost tile
            while j >= 0:
                #keep track of zero tile number
                if row[j] == 0:
                    zeros += 1
                    j -= 1
                    continue
                #start moving tiles to the chosen direction when reaching a non-zero tile
                if zeros > 0:
                    self.switch((i,j),zeros,"right")
                    j = 3
                    zeros = 0
                    continue
                #check if the current tile can be merged with the tile on its right side
                if self.merged((i,j),"right"):
                    break
                j -= 1
        if not self._copy:
            row,col = random.choice(list(self._empty_tiles))
            value = random.choice(self._random_list)
            self._board[row][col] = value
            self._empty_tiles.remove((row,col))
            if self.no_empty_tiles():
                self._end_game = True
                return f"Game over! Best score: {self._score}"
            else:
                return self.__str__()
    
    def move_up(self):
        #loof through the board in column order, with j being the column index, i being the row index
        for j in range(4):
            zeros = 0
            i = 0
            while i <= 3:
                #keep track of the number of zero tiles
                if self._board[i][j] == 0:
                    zeros += 1
                    i += 1
                    continue
                #start moving tiles to the chosen direction when reaching a non-zero tile
                if zeros > 0:
                    self.switch((i,j),zeros,"up")
                    i = 0
                    zeros = 0
                    continue
                #Check if the current tile can be merged with the tile above it
                if self.merged((i,j),"up"):
                    break
                i += 1
        if not self._copy:
            row,col = random.choice(list(self._empty_tiles))
            value = random.choice(self._random_list)
            self._board[row][col] = value
            self._empty_tiles.remove((row,col))
            if self.no_empty_tiles():
                self._end_game = True
                return f"Game over! Best score: {self._score}"
            else:
                return self.__str__()
    def move_down(self):
        #loof through the board in column order, with j being the column index, i being the row index
        for j in range(4):
            zeros = 0
            i = 3
            while i >= 0:
                #keep track of the number of zero tiles
                if self._board[i][j] == 0:
                    zeros += 1
                    i -= 1
                    continue
                #start moving tiles to the chosen direction when reaching a non-zero tile
                if zeros > 0:
                    self.switch((i,j),zeros,"down")
                    i = 3
                    zeros = 0
                    continue
                #Check if the current tile can be merged with the tile above it
                if self.merged((i,j),"down"):
                    break
                i -= 1
        if not self._copy:
            row,col = random.choice(list(self._empty_tiles))
            value = random.choice(self._random_list)
            self._board[row][col] = value
            self._empty_tiles.remove((row,col))
            if self.no_empty_tiles():
                self._end_game = True
                return f"Game over! Best score: {self._score}"
            else:
                return self.__str__()

    def no_empty_tiles(self):
        return len(self._empty_tiles) == 0
    
    def end_game(self):
        return self._end_game
    
    def __str__(self):
        return f"{self._board[0]}\n{self._board[1]}\n{self._board[2]}\n{self._board[3]}\n"
    
    #heuristic function to evaluate the game state
    def heuristic(self):
        res = 0
        for i in range(4):
            for j in range(4):
                res += self._board[i][j]*self._weight[i][j]
        res *= pow(len(self._empty_tiles),2) 
        return res
