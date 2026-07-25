import random
class Board:
    weight = [[pow(4,3),pow(4,2),pow(4,1),pow(4,0)],[pow(4,4),pow(4,5),pow(4,6),pow(4,7)],[pow(4,11),pow(4,10),pow(4,9),pow(4,8)],[pow(4,12),pow(4,13),pow(4,14),pow(4,15)]]
    def __init__(self,board = None):
        self._board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] if board == None else board

    def init_board(self):
        row,col = (random.randint(0,3),random.randint(0,3))
        value = random.choices([2,4], weights = [0.9,0.1])
        self._board[row][col] = value[0]

    def board(self):
        return self._board

    def set_value(self,pos,value):
        self._board[pos[0]][pos[1]] = value
    def get_value(self,pos):
        return self._board[pos[0]][pos[1]]
#function to move all tiles of a column or row to a certain direction
    def switch(self,pos: tuple, move: int, direction: str):
        x,y = pos[0], pos[1]
        if direction == "left":
            start = y-move
            for i in range(start,4):
                if i >= 4-move:
                    self._board[x][i] = 0
                else:
                    self._board[x][i] = self._board[x][i+move]

        elif direction == "right":
            start = y + move
            for i in range(start,-1,-1):
                if i < move:
                    self._board[x][i] = 0
                else:
                    self._board[x][i] = self._board[x][i-move]

        elif direction == "up":
            start = x-move
            for i in range(start,4):
                if i >= 4-move:
                    self._board[i][y] = 0
                else:
                    self._board[i][y] = self._board[i+move][y]

        elif direction == "down":
            start = x + move
            for i in range(start,-1,-1):
                if i < move:
                    self._board[i][y] = 0
                else:
                    self._board[i][y] = self._board[i-move][y]

    def merged(self,pos,direction):
        x,y = pos[0], pos[1]
        if direction == "left" and y > 0 and self._board[x][y] == self._board[x][y-1]:
            self._board[x][y-1] *= 2
            self.switch((x,y+1),1,direction)
            return self._board[x][y-1]
        if direction == "right" and y < 3 and self._board[x][y] == self._board[x][y+1]:
            self._board[x][y+1] *= 2
            self.switch((x,y-1),1,direction)
            return self._board[x][y+1]
        if direction == "up" and x > 0 and self._board[x][y] == self._board[x-1][y]:
            self._board[x-1][y] *= 2
            self.switch((x+1,y),1,direction)
            return self._board[x-1][y]
        if direction == "down" and x < 3 and self._board[x][y] == self._board[x+1][y]:
            self._board[x+1][y] *= 2
            self.switch((x-1,y),1,direction)
            return self._board[x+1][y]
        
    def find_empty_tiles(self):
        empty_tiles = []
        for i in range(4):
            for j in range(4):
                if self._board[i][j] == 0:
                    empty_tiles.append((i,j))
        return empty_tiles   

    def possible_merge(self):
        for i in range(4):
            for j in range(4):
                if i < 3 and self._board[i][j] == self._board[i+1][j]:
                    return True
                if j < 3 and self._board[i][j] == self._board[i][j+1]:
                    return True
        return False

    def in_terminal_state(self):
        if len(self.find_empty_tiles()) > 0:
            return False
        return not self.possible_merge()

    def create_new_tile(self, pos, value = None):
        x,y = pos[0], pos[1]
        if not value:
            self._board[x][y] = random.choices([2,4],weights = [0.9,0.1])
        else:
            self._board[x][y] = value

    def move_left(self):
        point = 0
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
                merged = self.merged((i,j),"left")
                if merged:
                    point += merged
                    break
                j += 1
        return point
        

    def move_right(self):
        point = 0
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
                merged = self.merged((i,j),"right")
                if merged:
                    point += merged
                    break
                j -= 1
        return point
    
    def move_up(self):
        point = 0
        #loof through the board in column order, with j being the column index, i being the row index
        for j in range(4):
            zeros = 0
            i = 0
            point = 0
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
                merged = self.merged((i,j),"up")
                if merged:
                    point += merged
                    break
                i += 1
        return point
    
    def move_down(self):
        point = 0
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
                merged = self.merged((i,j),"down")
                #Check if the current tile can be merged with the tile above it
                if merged:
                    point += merged
                    break
                i -= 1
        return point
    
    def set_new_tile(self,pos,value):
        row,col = pos
        self._board[row][col] = value

    def __str__(self):
        res = ""
        for i in range(len(self._board)):
            if i == len(self._board)-1:
                res += f"{self._board[i]}"
                continue
            res += f"{self._board[i]}\n"
        return res

    def monotonicity_score(self):
        score = 0
        for i in range(4):
            for j in range(4):
                if j < 3:
                    value_diff = self._board[i][j+1]-self._board[i][j]
                    if value_diff == 0:
                        continue
                    if value_diff/(self.weight[i][j]-self.weight[i][j+1]) > 0:
                        score += 1
                    else:
                        score -= 1
                if i < 3 and j in [0,3]:
                    value_diff = self._board[i][j]-self._board[i+1][j]
                    if value_diff == 0:
                        continue
                    if value_diff/(self.weight[i][j]-self.weight[i+1][j]) > 0:
                        score += 1
                    else:
                        score -= 1   
        return score

    def smoothness_score(self):
        score = 0
        for i in range(4):
            for j in range(4):
                if self._board[i][j] == 0:
                    continue
                for k in range(1,4-j):
                        if self._board[i][j+k] == 0:
                            continue
                        if self._board[i][j+k] <= self._board[i][j]:
                            score += (self._board[i][j+k]/self._board[i][j])
                            break
                        if self._board[i][j] <= self._board[i][j+k]:
                            score += (self._board[i][j]/self._board[i][j+k])
                            break
                if j in [0,3]:
                    for k in range(1,4-i):
                        if self._board[i+k][j] == 0:
                            continue
                        if self._board[i+k][j] <= self._board[i][j]:
                            score += (self._board[i+k][j]/self._board[i][j])
                            break
                        if self._board[i][j] <= self._board[i+k][j]:
                            score += (self._board[i+k][j]/self._board[i][j])
                            break
        return score       

    #heuristic function to evaluate the game state
    def heuristic(self):
        res = 0
        for i in range(4):
            for j in range(4):
                res += self._board[i][j]*self.weight[i][j]
        res += len(self.find_empty_tiles())
        return res

board = Board()
print(board)