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
        self.ai = AI()

    def test_new_game_created_correctly(self):
        self.ai.new_game(random_generator = self.Generator())
        self.assertEqual(self.ai.game.board.board, [[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], "Game board is not created properly!")

    def test_AI_makes_legal_move_right(self):
        self.ai.new_game(random_generator=self.Generator())
        self.assertEqual(self.ai.best_move(directions = ["left","right"]), "right", "Wrong return value from expectimax")

    def test_AI_makes_legal_move_up(self):
        self.ai.new_game(board = Board([[0,0,0,0],[0,0,0,0],[2,4,2,4],[4,2,4,2]]),random_generator = self.Generator())
        self.assertEqual(self.ai.best_move(3), "up", "AI did not make a legal move")

    def test_no_legal_move(self):
        self.ai.new_game(board = Board([[2,4,8,16],[4,256,128,1024],[2048,32,4,2],[2,8,16,4]]))
        self.assertIsNone(self.ai.best_move(), "best_move should not return value for boards in terminal state!")    

    def test_AI_makes_best_move_left(self):
        self.ai.new_game(Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]), self.Generator())
        self.assertEqual(self.ai.best_move(), "left", "AI did not make the best move")

    def test_AI_makes_best_move_down(self):
        self.ai.new_game(random_generator = self.Generator())
        self.assertEqual(self.ai.best_move(), "down", "AI did not make the best move")

    def test_expectimax_final_depth_returns_correct_value(self):
        board = Board([[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.assertEqual(self.ai.expectimax(True, board, 0,0), Board([[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]).heuristic())

    def test_expectimax_returns_correct_value_at_chance_node(self):
        board = Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        self.assertEqual(self.ai.expectimax(False, board, 0, 1), 0.9*Board([[2, 2, 8, 4],[2, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]).heuristic()+0.1*Board([[2, 2, 8, 4],[4, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]).heuristic(), "Chance nodes return wrong value!")

    def test_expectimax_returns_correct_value_at_max_node(self):
        board = Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_right = Board([[0, 4, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_left = Board([[4, 8, 4, 0],[4, 32, 8,0],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_down = Board([[0, 2, 8, 4],[2, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board_go_up = Board([[2, 2, 8, 4],[4, 4, 32, 8],[256, 32, 2, 4],[0, 4, 256, 2048]])
        self.assertEqual(self.ai.expectimax(True, board, 2, 3), max(board_go_right.heuristic(),board_go_left.heuristic(),board_go_down.heuristic(),board_go_up.heuristic()))

    def test_expectimax_has_correct_max_depth_15_empty_tiles(self):
        self.ai.new_game(random_generator = self.Generator())
        self.assertEqual(self.ai.best_move(given_max_depth = None, given_depth = 3), self.ai.game.board.heuristic())

    def test_expectimax_has_correct_max_depth_10_empty_tiles(self):
        self.ai.new_game(board = Board([[0,0,0,0],[0,0,0,8],[0,0,0,128],[256,512,1024,2048]]))
        self.assertEqual(self.ai.best_move(given_depth = 4), self.ai.game.board.heuristic())

    def test_expectimax_has_correct_max_depth_4_empty_tiles(self):
        self.ai.new_game(board = Board([[0,0,0,8],[0,4,2,8],[16,32,64,128],[256,512,1024,2048]]))
        self.assertEqual(self.ai.best_move(given_depth = 5), self.ai.game.board.heuristic())

    def test_expectimax_has_correct_max_depth_2_empty_tiles(self):
        self.ai.new_game(board = Board([[0,16,8,8],[0,4,2,8],[16,32,64,128],[256,512,1024,2048]]))
        self.assertEqual(self.ai.best_move(given_depth = 6), self.ai.game.board.heuristic())