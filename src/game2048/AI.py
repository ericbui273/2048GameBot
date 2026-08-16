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
        if board == None:
            self._game = Game(random_generator=random_generator)
            self._game.init_board()
        else:
            self._game = Game(board, random_generator)

    @property
    def game(self):
        return self._game

    def best_move(self, given_max_depth = None, given_depth = None, directions = ("left","right","up","down"), game = None):
        """Finds the best move from the given lists of moves

        Args:
            given_max_depth: maximum depth of the search tree, if no value is given the max depth is defined inside the function
            given_depth: the depth to start expectimax at, if no value is given, expectimax starts at depth 0
            directions: possible moves to evaluate
            game: the Game object to play, use the class attribute
            if no game is given

        Returns: the best move found from executing expectimax
        """
        if given_max_depth == None:
            find_empty_tiles = self._game.board.find_empty_tiles()
            empty_tiles_left = len(find_empty_tiles) if find_empty_tiles else 0
            if empty_tiles_left >= 12:
                max_depth = 3
            elif empty_tiles_left >= 8:
                max_depth = 4
            elif empty_tiles_left >= 4:
                max_depth = 5
            else:
                max_depth = 6
        else:
            max_depth = given_max_depth
        copy_board = copy.deepcopy(self._game.board) if game == None else copy.deepcopy(game.board)
        return self.expectimax(True, copy_board, 0, max_depth, directions) if not given_depth else self.expectimax(True, copy_board, given_depth, max_depth, directions)
    
    def expectimax(self, is_max:bool, board : Board, depth,max_depth, directions = ("left","right","up","down")):
        """Search the game tree to find the best move

        Args:
            root_node (Node): the root node containing the current board state
            depth: search depth, increase by 1 after each search
            max_depth: maximum search depth 
            directions: moves to find best move from
        Returns: the best move (left/right/up/down) or None if there is no legal move
        """
        if depth == max_depth:
            return board.heuristic()
        if is_max:
            move = None
            best_value = 0
            for d in directions:
                copy_board = copy.deepcopy(board)
                if d == "left":
                    copy_board.move_left()
                    if copy_board.board == board.board:
                        continue
                    cur_value = self.expectimax(False, copy_board, depth+1, max_depth)
                    best_value = cur_value
                    move = d
                if d == "right":
                    copy_board.move_right()
                    if copy_board.board == board.board:
                        continue
                    cur_value = self.expectimax(False, copy_board, depth+1, max_depth)
                    if cur_value > best_value:
                        best_value = cur_value
                        move = d
                if d == "up":
                    copy_board.move_up()
                    if copy_board.board == board.board:
                        continue
                    cur_value = self.expectimax(False, copy_board, depth+1, max_depth)
                    if cur_value > best_value:
                        best_value = cur_value
                        move = d   
                if d == "down":
                    copy_board.move_down()
                    if copy_board.board == board.board:
                        continue
                    cur_value = self.expectimax(False, copy_board, depth+1, max_depth)
                    if cur_value > best_value:
                        best_value = cur_value
                        move = d             
            if move is None:
                return board.heuristic() if depth != 0 else None
            return best_value if depth != 0 else move
        else:
            empty_tiles = board.find_empty_tiles()
            sum_value = 0 #each computed value of the child boards will be added
            for i,j in empty_tiles:
            # We loop through [(0.9,2),(0.1,4)] because in 2048, after each move, 
            # the new random tile has 90% possibility to be 2 and 10% possibility to be 4
                for val in [(0.9,2),(0.1,4)]:
                    probability, value = val[0], val[1]
                    copy_board = copy.deepcopy(board)
                    copy_board.set_value((i,j),value)
                    sum_value += probability/len(empty_tiles)*self.expectimax(True, copy_board, depth+1, max_depth)
            return sum_value
