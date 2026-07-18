from game_board import Board
class Node():
    def __init__(self,is_max,board:Board,value=None, children = []):
        self._is_max = is_max
        self._value = value
        self.children = children
        self.board = board
    
    def add_child(self,child):
        self.children.append(child)

    def get_board_copy(self):
        return (self.board.board().copy(),self.board.empty_tiles().copy())

    def set_value(self,value):
        self._value = value
    
    def value(self):
        return self._value