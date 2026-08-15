import unittest
from game2048.game import Game
from game2048.board import Board
class TestGame(unittest.TestCase):
    class Generator():
        def randint(self, a, b):
            return 0
        def choices(self,seq: list, weights: list):
            return [1024]
        def choice(self,seq = None):
            return seq[0]
    def setUp(self):
        self.new_game = Game(random_generator = self.Generator())
        self.game = Game(Board([[0,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,0,0]]), self.Generator(), 10)

    def test_constructor_creates_correct_game(self):
        self.assertEqual(self.game.board.board, [[0,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,0,0]], "The board should be created similarly with the given parameter")
        self.assertEqual(self.game.score, 10, "Score should be equal to the given parameter.")

    def test_constructor_creates_correct_new_game(self):
        self.assertEqual(self.new_game.board.board, [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], "Board should be blank if no board parameter is given to the constructor")
    def test_initialize_board_correctly(self):
        self.new_game.init_board()
        self.assertEqual(self.new_game.board.board, [[1024,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], "init_board not working properly")
        self.game.init_board()
        self.assertEqual(self.game.board.board, [[1024,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,0,0]], "init_board not working properly")

    def test_copy_board_correctly(self):
        copy_board = self.game.copy_board()
        self.assertEqual(self.game.board.board, copy_board.board, "Copied board should be identical to the original board!")
        self.assertFalse(self.game.board is copy_board, "Copied board should be a separate board")

    def test_move_left_correctly(self):
        self.game.make_move("left")
        self.assertEqual(self.game.board.board, [[1024,0,0,0],[4,8,0,0],[8,0,0,0],[0,0,0,0]], "Left move returns wrong board")
        self.assertEqual(self.game.score,22, "Left move returns wrong score!")

    def test_move_right_correctly(self):
        self.game.board.set_value((2,1),8)
        self.game.make_move("right")
        self.assertEqual(self.game.board.board, [[1024,0,0,0],[0,0,4,8],[0,0,0,16],[0,0,0,0]], "Right move returns wrong board")
        self.assertEqual(self.game.score, 38, "Right move returns wrong score")

    def test_move_up_correctly(self):
        game = Game(Board([[32,0,0,0],[32,0,0,0],[128,0,0,8],[128,0,0,0]]), self.Generator())
        game.make_move("up")
        self.assertEqual(game.board.board,[[64,1024,0,8],[256,0,0,0],[0,0,0,0],[0,0,0,0]], "Up move returns wrong board")
        self.assertEqual(game.score, 320, "Up move returns wrong score")

    def test_move_down_correctly(self):
        game = Game(Board([[32,0,0,8],[0,0,0,0],[32,0,0,8],[128,0,0,0]]), self.Generator())
        game.make_move("down")
        self.assertEqual(game.board.board, [[1024,0,0,0],[0,0,0,0],[64,0,0,0],[128,0,0,16]], "Down move returns wrong board")
        self.assertEqual(game.score, 80, "Down move returns wrong score")

    def test_new_game_not_over(self):
        self.assertFalse(self.game.game_over(), "A new game should return False for game_over!")

    def test_full_board_not_game_over(self):
        game = Game(Board([[2,4,8,16],[4,256,128,1024],[2048,32,4,2],[2,8,16,2]]))
        self.assertFalse(game.game_over(), "game_over returns incorrect value!")

    def test_game_over(self):
        game = Game(Board([[2,4,8,16],[4,256,128,1024],[2048,32,4,2],[2,8,16,4]]))
        self.assertTrue(game.game_over(), "game over returns incorrect value!")