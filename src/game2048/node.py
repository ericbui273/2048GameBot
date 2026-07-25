from board import Board
class Node():
    def __init__(self,is_max,board:Board, children = None):
        self._is_max = is_max
        self._children = [] if not children else children
        self._board = board
        self._value = 0
    
    def board(self):
        return self._board

    def add_child(self,child):
        self._children.append(child)

    def children(self):
        return self._children

    def set_value(self,value):
        self._value = value
    
    def value(self):
        return self._value