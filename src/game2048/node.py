from game2048.board import Board
class Node():
    """A class that maintains a node in the expectimax game tree

    Attributes:
        is_max: True if the node is a max node, 
        False if the node is a chance node
        children: list of children
        board: the board saved in the node
        value: heuristic value of the node's board
    """
    def __init__(self,is_max,board:Board, children = None):
        self._is_max = is_max
        self._children = [] if not children else children
        self._board = board
        self._value = 0

    @property
    def board(self):
        return self._board

    def add_child(self,child):
        self._children.append(child)

    @property
    def children(self):
        return self._children

    @property
    def is_max(self):
        return self._is_max
    
    def set_value(self,value):
        self._value = value

    @property
    def value(self):
        return self._value