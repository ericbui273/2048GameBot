from game_board import Board
from node import Node
class AI():
    def __init__(self):
        self._board = Board(False)
    
    def play(self,max_depth):
        if self._board.end_game:
            return
        board = self._board.board()
        empty_tiles = self._board.empty_tiles()
        self._game_tree = Node(is_max = True, board = Board(True,board,empty_tiles))
        return self.expectimax(self._game_tree,0,max_depth,True)
    
    def expectimax(self, root_node: Node, depth,max_depth, is_max):
        if depth == max_depth:
            return root_node.board.heuristic()
        board, empty_tiles = root_node.get_board_copy()
        if is_max:
            for d in ("left","right","up","down"):
                copy_board = Board(True,board,empty_tiles)
                if d == "left":
                    copy_board.move_left()
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
                if d == "right":
                    copy_board.move_right()
                    child_node = Node(False,copy_board)
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
                if d == "up":
                    copy_board.move_up()
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
                if d == "down":
                    copy_board.move_down()
                    if depth == 0:
                        child = (d,child_node)
                    else:
                        child = child_node
                    root_node.add_child(child)
                    child_node.set_value(self.expectimax(child_node,depth+1,max_depth,False))
            value = 0
            for child in root_node.children:
                if depth == 0:
                    value = max(value,child[1].value())
                else:
                    value = max(value,child.value())
            print(f"depth: {depth}, state: {value}")
            return value
        else:
            empty_tiles_copy = empty_tiles.copy()
            for pos in empty_tiles_copy:
                x,y = pos
                empty_tiles.remove(pos)
                copy = board.copy()
                for i in [(0.9,2),(0.1,4)]:
                    copy[x][y] = i[1]
                child = (i[0],Node(True,Board(copy,empty_tiles)))
                root_node.add_child(child)
                child[1].set_value(self.expectimax(child[1],depth+1,max_depth,True))
            value = 0
            for child in root_node.children:
                value += child[0]*child[1].value()
            value /= len(empty_tiles_copy)
            print(f"depth: {depth}, value:{value}")
            return value

ai = AI()
print(ai.play(0))