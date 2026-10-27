import random


class Board:
    """A class that maintains the game board and calculates heuristic value of specific board states

    Attributes:
        board: the game board to be maintained
        weight: class variable - a snake-shaped weight matrix used to calculate 
            the weighted sum of all the tiles, as part of the heuristic value

    """
    weight = [[pow(4,3),pow(4,2),pow(4,1),pow(4,0)],
              [pow(4,4),pow(4,5),pow(4,6),pow(4,7)],
              [pow(4,11),pow(4,10),pow(4,9),pow(4,8)],
              [pow(4,12),pow(4,13),pow(4,14),pow(4,15)]]


    def __init__(self, board: list | None = None):
        """Class constructor creating a new game board

        Args:
            board: the board to be created. If no board is given the class creates an empty board
        """
        self._board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] if board is None else board


    def init_board(self, generator = random.Random()):
        """Gives the first random value to the newly created empty board

        Args:
            generator (class): the class containing methods to generate random values. 
                Normally random.Random()
        """
        row,col = (generator.randint(0,3),generator.randint(0,3))
        value = generator.choices([2,4], weights = [0.9,0.1])
        self._board[row][col] = value[0]


    @property
    def board(self):
        return self._board


    def set_value(self, pos:tuple, value:int):
        self._board[pos[0]][pos[1]] = value


    def get_value(self, pos: tuple):
        return self._board[pos[0]][pos[1]]


    def switch(self,pos: tuple, move: int, direction: str):
        """Moves all tiles of a column or row to a certain direction

        Args:
            pos (tuple): position of the first tile to be moved
            move (int): how many cells are the tiles moved at a time
            direction (str): the moving direction, left/right/up/down
        """
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
        else:
            start = x + move
            for i in range(start,-1,-1):
                if i < move:
                    self._board[i][y] = 0
                else:
                    self._board[i][y] = self._board[i-move][y]



    def merged(self,pos: tuple, direction: str) -> int | None:
        """Check if the tile at a specific position can be merged with another adjacent tile

        Args:
            pos: position of the tile to be checked for merging
            direction: direction to which the adjacent tile is checked

        Returns:
            The value of the new merged tile if a merge is made, None if no merge is made  
        """
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
        return None


    def move(self, direction: str) -> int:
        """Alternate the game board according to the chosen move

        Args:
            direction (str): the move direction player makes

        Returns:
            The points made from the move (calculated based on merged value)
            If the move makes no merge, point = 0
        """
        point = 0
        for i in range(4):
            zeros = 0
            if direction in ("left, right"):
                row = self._board[i]
                j = 0 if direction == "left" else 3
                while ((j <= 3 and direction == "left")
                       or (j >= 0 and direction == "right")):
                    if row[j] == 0:
                        zeros += 1
                        j = j + 1 if direction == "left" else j - 1
                        continue
                    if zeros > 0:
                        self.switch((i,j), zeros, direction)
                        j = 0 if direction == "left" else 3
                        zeros = 0
                        continue
                    merged = self.merged((i,j), direction)
                    if merged:
                        point += merged
                    j = j + 1 if direction == "left" else j - 1
            else:
                j = 0 if direction == "up" else 3
                while ((j <= 3 and direction == "up")
                       or (j >= 0 and direction == "down")):
                    if self._board[j][i] == 0:
                        zeros += 1
                        j = j + 1 if direction == "up" else j - 1
                        continue
                    if zeros > 0:
                        self.switch((j,i), zeros, direction)
                        j = 0 if direction == "up" else 3
                        zeros = 0
                        continue
                    merged = self.merged((j,i), direction)
                    if merged:
                        point += merged
                    j = j + 1 if direction == "up" else j - 1
        return point


    def find_empty_tiles(self) -> list | None:
        empty_tiles = []
        for i in range(4):
            for j in range(4):
                if self._board[i][j] == 0:
                    empty_tiles.append((i,j))
        return empty_tiles if len(empty_tiles) > 0 else None


    def possible_merge(self) -> bool:
        """Check a full board to see if there are any 2 tiles that can be merged

        Returns:
            True if there are still mergeable tiles, False if the board is already in terminal state
        """
        for i in range(4):
            for j in range(4):
                if i < 3 and self._board[i][j] == self._board[i+1][j] and self._board[i][j] != 0:
                    return True
                if j < 3 and self._board[i][j] == self._board[i][j+1] and self._board[i][j] != 0:
                    return True
        return False


    def in_terminal_state(self) -> bool:
        """Check if a board is in terminal state

        Returns:
            False if there are still empty tiles or mergeable tiles in the board,
            True if there are none 
        """
        if self.find_empty_tiles():
            return False
        return not self.possible_merge()


    def __str__(self):
        res = ""
        for i in range(len(self._board)):
            if i == len(self._board)-1:
                res += f"{self._board[i]}"
                continue
            res += f"{self._board[i]}\n"
        return res


    def heuristic(self) -> int:
        """Heuristic function to evaluate the state of the game board,
        calculated using the snake-shaped weight matrix (class variable)

        Returns: heuristic value
        """
        res = 0
        for i in range(4):
            for j in range(4):
                res += self._board[i][j]*self.weight[i][j]
        return res
