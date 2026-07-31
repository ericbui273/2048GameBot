import unittest
from game2048.game import Game
from game2048.board import Board
from game2048.AI import AI
from game2048.node import Node
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

    def test_AI_makes_legal_move(self):
        self.ai.new_game(random_generator=self.Generator())
        self.assertEqual(self.ai.best_move(4,["left","right"]), "right", "Wrong return value from expectimax")

    def test_AI_makes_best_move(self):
        self.ai.new_game(Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]), self.Generator())
        self.ai.play(4,False)
        self.assertEqual(self.ai.game.board.board, [[4, 8, 4, 1024],[4, 32, 8, 0],[4, 32, 2, 4],[256, 4, 256, 2048]], "AI did not make the best move")

    def test_play_loop_stops_when_game_over(self):
        self.ai.new_game(Board([[2, 2, 8, 4],[8, 16, 32, 16],[32, 128, 64, 32],[256, 1024, 2048, 4096]]))
        self.ai.play(4)
        self.assertTrue(self.ai.game.game_over(), "Play loop at continuous state must stop only when the game is over!")

    def test_expectimax_final_depth_returns_correct_value(self):
        root_node = Node(is_max = True, board = Board([[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
        self.assertEqual(self.ai.expectimax(root_node, 0,0), Board([[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]).heuristic())

    def test_expectimax_returns_correct_value_at_chance_node(self):
        root_node = Node(is_max = False, board = Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]))
        self.assertEqual(self.ai.expectimax(root_node,0,1), 0.9*Board([[2, 2, 8, 4],[2, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]).heuristic()+0.1*Board([[2, 2, 8, 4],[4, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]).heuristic(), "Chance nodes return wrong value!")

    def test_expectimax_returns_correct_value_at_max_node(self):
        root_node = Node(is_max = True, board = Board([[2, 2, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]]))
        board1 = Board([[0, 4, 8, 4],[0, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board2 = Board([[4, 8, 4, 0],[4, 32, 8,0],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board3 = Board([[0, 2, 8, 4],[2, 4, 32, 8],[4, 32, 2, 4],[256, 4, 256, 2048]])
        board4 = Board([[2, 2, 8, 4],[4, 4, 32, 8],[256, 32, 2, 4],[0, 4, 256, 2048]])
        self.assertEqual(self.ai.expectimax(root_node,2,3), max(board1.heuristic(),board2.heuristic(),board3.heuristic(),board4.heuristic()))