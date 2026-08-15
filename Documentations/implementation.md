# Implementation documentation

## Program structure
The program creates and maintains a 2048 game board using the `Board` class, creates and makes sure the game progresses with the correct logic using the `Game` class, and controls behaviour of the AI using the `AI` class. The expectimax algorithm used to find out the best move possible is also performed inside the `AI` class.

In addition, the user experience is managed by the `GUI` class. The `GUI` class allows users to choose the mode of the game, including at which optimal level the AI plays and whether the AI plays at continuous mode (without user's interruption) or step mode (user presses SPACE for the AI to continue playing).

## Space and time complexity
General expectimax's time complexity: **_O(b<sup>m</sup>)_** for b is the branching factor and m is the maximum depth of the search

At each round, several for loops on the board are implemented, which add to the overall runtime. However, each for loops takes O(1) time since it does not change when the branching factor or max search depth changes. Therefore, they do not affect the time complexity of expectimax.

## Rooms for improvement
There are still a few things I had planned to but was not able to implement on time during the project period. First of all, the heuristic function could still be improved. Even though with the current heuristic function, the game can already reach 2048 most of the time, and half of the time to at least 4096, it still only takes into consideration the value distribution of the board. If the function can be developed to consider also the smoothness, monotonicity and number of empty tiles, the results can be even better. However, within the scope of the project, I have to prioritize maximizing expectimax over coming up with the perfect heuristic function.

In addition, even though I try to make my code as clear and well-structured as possible, it could still benefit from some refactoring. Some of the classes are currently holding quite a lot of responsibilities (e.g. class Board is responsible for both maintaining the board and evaluates its state and heuristic value, class AI manages both behaviours of the AI and the recursive expectimax search for the best moves). This is still fine within the scope of this project, but I believe it could cause difficulties and confusions if I develop the program to a more complex level. In the future I might think of some ways to make the classes lighter and make the class roles clearer and more understandable.

## Use of large language models (LLM) as source of support
I used GPT-5.5 and -5.6 for troubleshooting when setting up Poetry and resolving related environment and dependency issues since Poetry and the concept of virtual environment are totally new to me. I also came to chatGPT occasionally for questions about unfamiliar concept, such as differences between Pip and Poetry, import issues in complex projects in Python, and so on. 

In addition, I used Claude Sonnet 5 to write the GUI class since GUI is not the main topic of this course, and there is no suitable existing open-source GUI implementation for 2048. The use of LLMs for this part was confirmed as acceptable by my instructor.

In general, LLMs were used as a supporting tool during the project. The core functionalities of the program, including the classes Board, Game, AI, and the unit tests were all designed and implemented by me.
