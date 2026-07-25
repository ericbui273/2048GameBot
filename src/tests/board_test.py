import unittest
from game2048.board import Board
class TestBoard(unittest.TestCase):
    def setUp(self):
        print("Set up goes here")

    def test_hello_world(self):
        self.assertTrue(3>1)