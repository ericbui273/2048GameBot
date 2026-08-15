import unittest
from game2048.board import Board
class TestBoard(unittest.TestCase):
    def setUp(self):
        self.blank_board = Board()
        self.board = Board([[0,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,0,0]])

    def test_constructor_creates_correct_board(self):
        self.assertEqual(str(self.blank_board), f"[0, 0, 0, 0]\n[0, 0, 0, 0]\n[0, 0, 0, 0]\n[0, 0, 0, 0]", "The board should be blank when no parameter is given to the class constructor")
        self.assertEqual(self.board.board, [[0,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,0,0]], "The board is different from the given parameter!")

    def test_set_correct_value(self):
        self.board.set_value((3,2),8)
        self.assertEqual(self.board.board,[[0,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,8,0]])

    def test_get_correct_value(self):
        self.assertEqual(self.board.get_value((1,1)),2, "get_value() returns incorrect value!")

    def test_init_board_correctly(self):
        class Generator():
            def randint(self, a, b):
                return 0
            def choices(self,seq: list, weights: list):
                return [1024]
        generator = Generator()
        self.board.init_board(generator)
        self.assertEqual(self.board.board,[[1024,0,0,0],[2,2,4,4],[0,0,8,0],[0,0,0,0]], "Left move incorrect!")

    def test_board_moves_left_double_merge(self):
        self.board.move_left()
        self.assertEqual(self.board.board,[[0,0,0,0],[4,8,0,0],[8,0,0,0],[0,0,0,0]], "Left move incorrect!")

    def test_board_moves_left_single_merge(self):
        self.board.set_value((1,2),2)
        self.board.move_left()
        self.assertEqual(self.board.board,[[0,0,0,0],[4,2,4,0],[8,0,0,0],[0,0,0,0]], "Left move incorrect!")

    def test_board_moves_left_with_empty_tile_in_between(self):
        board = Board([[0,2,0,4],[0,0,0,0],[0,0,0,0],[2,0,2,4]])
        board.move_left()
        self.assertEqual(board.board, [[2,4,0,0],[0,0,0,0],[0,0,0,0],[4,4,0,0]], "Left move incorrect!")

    def test_board_moves_left_no_merge(self):
        self.blank_board.set_value((2,0),7)
        self.blank_board.set_value((2,2),16)
        self.blank_board.move_left()
        self.assertEqual(self.blank_board.board, [[0,0,0,0],[0,0,0,0],[7,16,0,0],[0,0,0,0]], "Left move incorrect!")

    def test_move_left_double_merge_score(self):
        self.assertEqual(self.board.move_left(), 12, "Left move returns wrong score!")

    def test_move_left_two_merges_score(self):
            board = Board([[0,8,0,8],[0,0,0,0],[32,0,32,0],[0,0,0,0]])
            self.assertEqual(board.move_left(), 80, "Left move returns wrong score!")

    def test_move_left_single_merge_score(self):
        self.board.set_value((1,0),0)
        self.assertEqual(self.board.move_left(),8, "Left move returns wrong score!")

    def test_move_left_no_merge_score(self):
        self.blank_board.set_value((2,0),7)
        self.blank_board.set_value((2,2),16)
        self.assertEqual(self.blank_board.move_left(), 0, "Left move returns wrong score!")

    def test_board_moves_right_with_empty_tile_in_between(self):
        board = Board([[8,0,16,0],[0,0,8,0],[0,0,0,0],[16,16,0,16]])
        board.move_right()
        self.assertEqual(board.board,[[0,0,8,16],[0,0,0,8],[0,0,0,0],[0,0,16,32]], "Right move incorrect!")

    def test_move_right_double_merge_score(self):
        self.assertEqual(self.board.move_right(),12, "Right move returns wrong score!")

    def test_move_right_no_merge_score(self):
        self.blank_board.set_value((2,0),7)
        self.blank_board.set_value((2,2),16)
        self.assertEqual(self.blank_board.move_right(), 0, "Right move returns wrong score!")        

    def test_board_moves_up_double_merge(self):
        board = Board([[32,0,0,0],[32,0,0,0],[128,0,0,8],[128,0,0,0]])
        board.move_up()
        self.assertEqual(board.board,[[64,0,0,8],[256,0,0,0],[0,0,0,0],[0,0,0,0]], "Up move incorrect!")

    def test_board_moves_up_with_empty_tile_in_between(self):
        board = Board([[0,0,16,0],[0,0,0,0],[0,0,16,0],[0,0,64,0]])
        board.move_up()
        self.assertEqual(board.board,[[0,0,32,0],[0,0,64,0],[0,0,0,0],[0,0,0,0]]), "Up move incorrect!"

    def test_move_up_double_merge_score(self):
        board = Board([[32,0,0,0],[32,0,0,0],[128,0,0,8],[128,0,0,0]])
        self.assertEqual(board.move_up(), 320, "Up move returns wrong score!")

    def test_move_up_no_merge_score(self):
        self.assertEqual(self.board.move_up(), 0, "Up move returns wrong score!")

    def test_board_moves_down_double_merge(self):
        board = Board([[0,0,32,0],[0,0,32,0],[0,0,128,8],[0,0,128,0]])
        board.move_down()
        self.assertEqual(board.board, [[0,0,0,0],[0,0,0,0],[0,0,64,0],[0,0,256,8]], "Down move incorrect!")

    def test_board_moves_down_with_empty_tile_in_between(self):
        board = Board([[0,0,128,0],[0,0,0,0],[0,0,128,0],[0,0,0,0]])
        board.move_down()
        self.assertEqual(board.board, [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,256,0]], "Down move incorrect!")

    def test_move_down_two_merges_score(self):
        board = Board([[0,1024,0,0],[0,1024,2048,0],[0,0,0,0],[0,1024,2048,0]])
        self.assertEqual(board.move_down(),2048+4096, "Down move returns wrong score!")

    def test_find_empty_tiles_no_empty_tile(self):
        board = Board([[2,4,8,16],[16,8,4,2],[2,2,2,2],[4,4,4,4,]])
        self.assertIsNone(board.find_empty_tiles(), "There is no empty tile!")

    def test_find_correct_empty_tiles(self):
        board = Board([[2,0,4,8],[32,16,0,64],[0,128,256,1024],[64,32,128,0]])
        self.assertEqual(board.find_empty_tiles(), [(0,1),(1,2),(2,0),(3,3)], "find_empty_tiles returns incorrect result")

    def test_find_correct_possible_merge(self):
        self.assertTrue(self.board.possible_merge(), "There are possible merges!")

    def test_no_possible_merge_on_blank_board(self):
        self.assertFalse(self.blank_board.possible_merge(), "No possible merge on blank board!")

    def test_no_possible_merge(self):
        board = Board([[2,4,8,16],[4,256,128,1024],[0,0,4,2],[0,0,2,4]])
        self.assertFalse(board.possible_merge(), "possible_merge() returns incorrect result!")

    def test_full_board_not_in_terminal_state(self):
        board = Board([[2,4,8,16],[4,256,128,1024],[2048,32,4,2],[2,8,16,2]])
        self.assertFalse(board.in_terminal_state(), "in_terminal_state returns incorrect output!")

    def test_board_in_terminal_state(self):
        board = Board([[2,4,8,16],[4,256,128,1024],[2048,32,4,2],[2,8,16,4]])
        self.assertTrue(board.in_terminal_state(), "in_terminal_state returns incorrect output!")

    def test_board_not_in_terminal_state(self):
        self.assertFalse(self.board.in_terminal_state(), "in_terminal_state returns incorrect output!")

    def test_heuristic_evaluates_correctly(self):
        board1 = Board([[0, 0, 0, 0],[0, 0, 0, 0],[8, 4, 0, 0], [128, 512, 1024, 2]])
        board2 = Board([[0, 0, 0, 2],[0,0,0,0],[0,0,8,4], [0, 128, 512, 1024]])
        self.assertTrue(board1.heuristic()<board2.heuristic(), "Heuristic function should not give higher score to the less advantageous board!")

    def test_heuristic_returns_correct_value(self):
        self.board.set_value((3,2),8)
        self.assertEqual(self.board.heuristic(),2149665280, "Incorrect heuristic value!")