import random
from game2048.board import Board


class Game():
    """A class that maintains a game
    
    Attributes:
        board: the game board
        random_generator: the class containing methods 
            to generate random values. Normally random.Random()
        score: current score of the game, increased after every merge
    """


    def __init__(self,
                 board: Board | None = None,
                 random_generator = random.Random(),
                 score: int | int = 0):
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


    @property
    def board(self):
        return self._board


    def make_move(self, direction: str):
        self._score += self._board.move(direction)
        pos = self._random.choice(self._board.find_empty_tiles())
        # There is always at least 1 empty tile after every move is made
        # because the AI makes sure to not consider
        # any move that does not change the board
        # Therefore, there is always a valid value for pos variable
        value = self._random.choices([2,4],weights = [0.9,0.1])
        self._board.set_value(pos,value[0])


    def game_over(self) -> bool:
        """Check if the board is in terminal state,
        and print the game over notice if the game is over

        Returns:
            whether the game is over
        """
        if self._board.in_terminal_state():
            return True
        return False
