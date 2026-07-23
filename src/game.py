from board import Board
import random
import copy
class Game():
    def __init__(self):
        self._board = Board()
        self._score = 0
        print(self._board)

    def board(self):
        return copy.deepcopy(self._board)

    def move_left(self):
        self._score += self._board.move_left()
        pos = random.choice(self._board.find_empty_tiles())
        value = random.choices([2,4],weights = [0.9,0.1])
        self._board.set_new_tile(pos,value[0])

    def move_right(self):
        print(self._board.move_right())
        pos = random.choice(self._board.find_empty_tiles())
        value = random.choices([2,4],weights = [0.9,0.1])
        self._board.set_new_tile(pos,value[0])

    def move_up(self):
        print(self._board.move_up())
        pos = random.choice(self._board.find_empty_tiles())
        value = random.choices([2,4],weights = [0.9,0.1])
        self._board.set_new_tile(pos,value[0])

    def move_down(self):
        print(self._board.move_down())
        pos = random.choice(self._board.find_empty_tiles())
        value = random.choices([2,4],weights = [0.9,0.1])
        self._board.set_new_tile(pos,value[0])

    def print_board(self):
        print(self._board)

    def game_over(self):
        if self._board.no_empty_tiles():
            print(f"Game over! Score: {self._score}")
            return True
        return False