from game2048.board import Board
import copy
import random
class Game():
    """A class that maintains a game
    
    Attributes:
        board: the game board
        random: the class containing methods to generate random values. Normally random.Random()
        score: current score of the game, increased after every merge
    """
    def __init__(self, board = None, random_generator = random.Random(), score = 0):
        self._board = board if board else Board()
        self._random = random_generator
        self._score = score

    def init_board(self):
        """Gives the first random value to the newly created empty board
        """
        self._board.init_board(self._random)

    @property
    def score(self):
        return self._score
        
    def copy_board(self):
        return copy.deepcopy(self._board)

    @property
    def board(self):
        return self._board

    def move_left(self):
        self._score += self._board.move_left()
        pos = self._random.choice(self._board.find_empty_tiles())
        value = self._random.choices([2,4],weights = [0.9,0.1])
        self._board.set_value(pos,value[0])
        print(f"{self._board}\n")

    def move_right(self):
        self._score += self._board.move_right()
        pos = self._random.choice(self._board.find_empty_tiles())
        value = self._random.choices([2,4],weights = [0.9,0.1])
        self._board.set_value(pos,value[0])
        print(f"{self._board}\n")

    def move_up(self):
        self._score += self._board.move_up()
        pos = self._random.choice(self._board.find_empty_tiles())
        value = self._random.choices([2,4],weights = [0.9,0.1])
        self._board.set_value(pos,value[0])
        print(f"{self._board}\n")

    def move_down(self):
        self._score += self._board.move_down()
        pos = self._random.choice(self._board.find_empty_tiles())
        value = self._random.choices([2,4],weights = [0.9,0.1])
        self._board.set_value(pos,value[0])
        print(f"{self._board}\n")

    def game_over(self):
        """Check if the board is in terminal state,
        and print the game over notice if the game is over

        Returns:
            whether the game is over
        """
        if self._board.in_terminal_state():
            print(f"Game over! Score: {self._score}")
            return True
        return False