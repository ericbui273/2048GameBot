from node import Node
from game import Game
import copy
class AI():
    def new_game(self):
        print("Start game")
        self._game = Game()
        
        self.play(3)

    def play(self,max_depth):
        while True:
            if self._game.game_over():
                break
            self._game_tree = Node(is_max = True, board = self._game.board())
            move = self.expectimax(self._game_tree,0,max_depth,True)[0]
            if move == "left":
                self._game.move_left()
            elif move == "right":
                self._game.move_right()
            elif move == "up":
                self._game.move_up()
            elif move == "down":
                self._game.move_down()
            move = input("Continue? ")
            if move == "no":
                break
    
    def expectimax(self, root_node: Node, depth,max_depth, is_max):
        if depth == max_depth:
            return root_node.board().heuristic()
        board = root_node.board()
        if is_max:
            for d in ("left","right","up","down"):
                copy_board = copy.deepcopy(board)
                if d == "left":
                    copy_board.move_left()
                    if copy_board.board() == board.board():
                        continue
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
                if d == "right":
                    copy_board.move_right()
                    if copy_board.board() == board.board():
                        continue
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
                if d == "up":
                    copy_board.move_up()
                    if copy_board.board() == board.board():
                        continue
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
                if d == "down":
                    copy_board.move_down()
                    if copy_board.board() == board.board():
                        continue    
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
            value = 0
            for child in root_node.children():
                if depth == 0:
                    if child[1].value() > value:
                        move = child[0]
                        value = child[1].value()
                elif depth > 0:
                    value = max(value,child.value())
            return value if depth != 0 else (move,value)
        else:
            for i in range(4):
                for j in range(4):
                    if board.get_value((i,j)) != 0:
                        continue
                    for val in [(0.9,2),(0.1,4)]:
                        copy_board = copy.deepcopy(board)
                        copy_board.set_value((i,j),val[1])
                        child_node = Node(True,copy_board)
                        child = (val[0],child_node)
                        root_node.add_child(child)
                        child_node.set_value(self.expectimax(child_node,depth+1,max_depth,True))
            value = 0
            for child in root_node.children():
                value += child[0]*child[1].value()
            value /= (len(root_node.children())/2)
            return value