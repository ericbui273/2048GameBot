import unittest
from game2048.game import Game
from game2048.board import Board
from game2048.AI import AI


class TestAI(unittest.TestCase):
    class Generator():
        def randint(self, a, b):
            return 0
        def choices(self,seq: list, weights: list):
            return [1024]
        def choice(self,seq = None):
            return seq[0]

    def setUp(self):
        self.new_ai = AI(game = Game(random_generator = self.Generator()))
        self.ai = AI(game = Game(board = Board([[0,0,0,0],[0,0,0,0],[2,4,2,4],[4,2,4,2]]), random_generator = self.Generator()))

    def test_new_game_created_correctly(self):
        self.new_ai.new_game()
        self.assertEqual(self.new_ai.game.board.board, [[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], "Game board is not created properly!")

    def test_AI_makes_legal_move_left(self):
        ai = AI(game = Game(board = Board([[0,0,0,1024],[0,0,0,0],[0,0,0,0],[0,0,0,0]])))
        self.assertEqual(ai.best_move(directions = ["left","right"]), "left", "Wrong return value from expectimax")

    def test_AI_makes_legal_move_up(self):
        self.assertEqual(self.ai.best_move(3), "up", "AI did not make a legal move")

    def test_no_legal_move(self):
        ai = AI(game = Game(board = Board([[2,4,8,16],[4,256,128,1024],[2048,32,4,2],[2,8,16,4]])))
        self.assertIsNone(ai.best_move(), "best_move should not return value for boards in terminal state!")    

    def test_AI_makes_best_move_right(self):
        def heuristic(board:list) -> int:
            res = 0
            for row in board:
                if 64 in row:
                    res += 100
            return res
        ai = AI(game = Game(board = Board([[2, 2, 8, 32], [0, 4, 16, 16], [4, 1024, 2, 0], [256, 1024, 2048, 0]])))
        self.assertEqual(ai.expectimax_max(ai._game.board, 0, 5, heuristic_func=heuristic), "right", "AI did not make the best move")

    def test_AI_makes_best_move_down(self):
        def heuristic(board:list) -> int:
            res = 0
            for row in board:
                if 2048 in row:
                    res = 100
                    break
            return res
        ai = AI(game=Game(board=Board([[2, 2, 8, 32], [0, 4, 16, 16], [512, 128, 1024, 0], [512, 1024, 64, 4096]])))
        self.assertEqual(self.new_ai.expectimax_max(ai._game.board,0,5,heuristic_func=heuristic), "down", "AI did not make the best move")

    def test_expectimax_final_depth_returns_correct_value(self):
        board = Board([[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.assertEqual(self.new_ai.expectimax_max(board, 0,0), Board([[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]).heuristic())

    def test_expectimax_returns_correct_value_at_chance_node(self):
        board = Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        self.assertEqual(self.ai.expectimax_chance(board, 0, 1), 0.9*Board([[2, 2, 8, 4],[2, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]).heuristic()+0.1*Board([[2, 2, 8, 4],[4, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]).heuristic(), "Chance nodes return wrong value!")

    def test_expectimax_returns_correct_value_at_max_node(self):
        board = Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_right = Board([[0, 4, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_left = Board([[4, 8, 4, 0],[4, 32, 8,0],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_down = Board([[0, 2, 8, 4],[2, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_up = Board([[2, 2, 8, 4],[4, 4, 32, 8],[256, 32, 2, 4],[0, 4, 256, 2048]])
        self.assertEqual(self.ai.expectimax_max(board, 2, 3), max(board_go_right.heuristic(),board_go_left.heuristic(),board_go_down.heuristic(),board_go_up.heuristic()))

    def test_expectimax_has_correct_max_depth_15_empty_tiles(self):
        self.new_ai.new_game()
        self.assertEqual(self.new_ai.best_move(given_max_depth = None, given_depth = 3), self.new_ai.game.board.heuristic()) 
        #with 15 empty tiles, default max depth is 3, so the best_move function at given depth 3 returns the heuristic value of the current board

    def test_expectimax_has_correct_max_depth_10_empty_tiles(self):
        ai = AI(game = Game(board = Board([[0,0,0,0],[0,0,0,8],[0,0,0,128],[256,512,1024,2048]])))
        self.assertEqual(ai.best_move(given_depth = 4), ai.game.board.heuristic())

    def test_expectimax_has_correct_max_depth_4_empty_tiles(self):
        ai = AI(game = Game(board = Board([[0,0,0,8],[0,4,2,8],[16,32,64,128],[256,512,1024,2048]])))
        self.assertEqual(ai.best_move(given_depth = 5), ai.game.board.heuristic())

    def test_expectimax_has_correct_max_depth_2_empty_tiles(self):
        ai = AI(game = Game(board = Board([[0,16,8,8],[0,4,2,8],[16,32,64,128],[256,512,1024,2048]])))
        self.assertEqual(ai.best_move(given_depth = 6), ai.game.board.heuristic())