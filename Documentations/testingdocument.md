# Test report
The classes Board, Game, AI in the directory src/game2048 were tested using unit tests. Class GUI was excluded from the unit testing.

**Unit testing coverage report**
<img width="813" height="193" alt="image" src="https://github.com/user-attachments/assets/cb4cd2e7-d346-452b-b2b5-d77052297b99" />


## Manual test using graphical user interface (GUI)
The game was run several times using GUI to verify from the user perspective that the AI makes legal moves and returns good results. 

<img width="455" height="458" alt="image" src="https://github.com/user-attachments/assets/d8fab182-79ec-4f3f-b391-5e7bc3ef531a" />

**Board reaches 8192 with default max search depth**

<img width="454" height="454" alt="image" src="https://github.com/user-attachments/assets/92479896-8625-4e8b-951d-06a8aa229cf4" />

**Board reaches 2048 with max search depth 4**

## Automated unit testing
### Class Board
The unit test for the class Board was made using both a blank board and boards that already has some values on it, with different boards used for different test cases. In addition, a self-defined version of random number generator was injected to control the output of the _**init_board()**_ function, which creates a new random tile

What has been tested:
- The constructor and all of the functions work properly
- Moves and merges are done correctly in different cases: when there is only one possible merge, when there are more than one possible merge, when there is no possible merge, and when there are empty tiles between two tiles
- The score is calculated correctly when there are merges made and when there is no mere, the score is 0
- Whether or not a board is in terminal state is decided correctly in different cases: when the board is full with and without possible merges, when the board is not full
- Whether or not there are possible merges is decided correctly in different cases: when the board is blank and when there are values on it
- Heuristic function returns correct value, and heuristic value of the more advantageous board is higher than the less advantageous one

### Class Game
The unit test for the class Game was made using different games that deal with either a blank board or a board that already has some values on it, depending on the test cases. In addition, a self-defined version of random number generator was injected to control the output after every move is made

What has been tested:
- The constructor and all of the functions work properly, the board is also initialized correctly with a random tile at the beginning of the game
- The four moves in four directions can all be made properly
- Whether a game is over is decided correctly in 3 different cases: when the board is full with and without possible merges and at the beginning of the game

### Class AI
The unit test for the class AI was made using different games with different boards to make sure the AI makes the best decision possible in all kinds of situation. In addition, a self-defined version of random number generator was injected to control the output after every move is made

What has been tested:
- The new game is created properly (with a blank board and a random tile created using the random number generator)
- The AI always makes legal move, the attempt to find a move for a board in terminal state will return None
- In situation where there are several legal moves, the AI makes the best move possible
- Expectimax conducts search with the correct maximum depth as defined in the best_move() function if no max depth value is given
- Expectimax returns correct value in 3 situations: at the final depth, at a chance node and at a max node


