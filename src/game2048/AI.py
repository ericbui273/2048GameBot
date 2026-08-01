from game2048.node import Node
from game2048.game import Game
from game2048.board import Board
import copy
import random
class AI():
    """A class that maintains the functionality of the AI in a game

    Attributes:
        game: the game that the AI is playing
    """
    def new_game(self, board = None, random_generator = random.Random()):
        """Start a new game, a new Game object is created

        Args:
            board: the current game board, board is empty if no given argue
            random_generator: the class containing methods to generate random values. 
            Normally random.Random()
        """
        print("Start game")
        if board == None:
            self._game = Game(random_generator=random_generator)
            self._game.init_board()
        else:
            self._game = Game(board, random_generator)

    @property
    def game(self):
        return self._game
    
    def play(self,max_depth,continuous = True):
        """AI starts playing when play is called

        Args:
            max_depth: maximum depth of the search tree
            continuous: whether the AI continues to play the game on its own,
            default value is True
        """
        while True:
            if self._game.game_over():
                break
            move = self.best_move(max_depth)
            if move == "left":
                self._game.move_left()
            elif move == "right":
                self._game.move_right()
            elif move == "up":
                self._game.move_up()
            elif move == "down":
                self._game.move_down()
            if not continuous:
                break

    def best_move(self, max_depth, directions = ("left","right","up","down"), game = None):
        """Finds the best move from the give list of move

        Args:
            max_depth: maximum depth of the search tree
            directions: possible moves to evaluate
            game: the Game object to play, use the class attribute
            if no game is given

        Returns: the best move found from executing expectimax
        """
        copy_board = copy.deepcopy(self._game.board) if game == None else copy.deepcopy(game.board)
        self._game_tree = Node(is_max = True, board = copy_board)
        return self.expectimax(self._game_tree, 0, max_depth, directions)
    
    def expectimax(self, root_node: Node, depth,max_depth, directions = ("left","right","up","down")):
        """Search the game tree to find the best move

        Args:
            root_node (Node): the root node containing the current board state
            depth: search depth, increase by 1 after each search
            max_depth: maximum search depth 
            directions: moves to find best move from
        Returns: the best move (left/right/up/down)
        """
        if depth == max_depth:
            return root_node.board.heuristic()
        board = root_node.board
        if root_node.is_max:
            for d in directions:
                copy_board = copy.deepcopy(board)
                if d == "left":
                    copy_board.move_left()
                    if copy_board.board == board.board:
                        continue
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth))
                if d == "right":
                    copy_board.move_right()
                    if copy_board.board == board.board:
                        continue
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth))
                if d == "up":
                    copy_board.move_up()
                    if copy_board.board == board.board:
                        continue
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth))
                if d == "down":
                    copy_board.move_down()
                    if copy_board.board == board.board:
                        continue    
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth))
            if root_node.children == []:
                return board.heuristic() if depth != 0 else None
            value = 0
            move = "left"
            for child in root_node.children:
                if depth == 0:
                    if child[1].value > value:
                        move = child[0]
                        value = child[1].value
                else:
                    value = max(value,child.value)
            return value if depth != 0 else move
        else:
            empty_tiles = board.find_empty_tiles()
            for i,j in empty_tiles:
                for val in [(0.9,2),(0.1,4)]:
                    copy_board = copy.deepcopy(board)
                    copy_board.set_value((i,j),val[1])
                    child_node = Node(True,copy_board)
                    child = (val[0],child_node)
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth))
            value = 0
            for child in root_node.children:
                value += child[0]*child[1].value
            value /= (len(root_node.children)/2)
            return value