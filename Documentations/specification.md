# 2048 Game Bot Specification Document
This project is for the course Algorithms and AI Lab as part of my study in the Bachelor's Programme of Science in University of Helsinki.

## General
In this project, I will implement a simple AI game bot to play 2048 optimally. The goal is for the bot to not only reach the 2048 tile but get as high value as possible while still ensuring time efficiency.
### Software functionalities
The implementation of the project includes developing a 2048 game interface, the game logic that merges the two adjacent tiles of same values and generates a new tile with 90% chance to be of value 2 and 10% chance to be of value 4, and an AI game bot capable of always choosing the best move possible. The core implementation of the project would be **the AI bot**.
### Programming language
The project will be done using Python. In addition, I can also peer-review projects written in Java.
### Received inputs
Since the AI does not play against a human in this game, there is no user input needed to implement the program.
## Algorithms and data structures
### For evaluating the game state
For evaluating the game state resulting from a specific move, I will implement a **heuristic evaluation function** that takes into account the value distribution of the board.



### For choosing the best next move
I will implement **expectimax** algorithm and a **game tree** data structure. The game tree consists of alternating **max nodes** (returning the highest values of their child nodes) and **chance nodes** (returning the expected values of their child nodes.

Expectimax **Big-O analysis** with branching factor as _b_ and the maximum depth of the tree as _m_:
- Time complexity: **_O(b<sup>m</sup>)_**
- Space complexity: **_O(b*m)_**

## Sources
[Expectimax algorithm in game theory](https://www.geeksforgeeks.org/dsa/expectimax-algorithm-in-game-theory/)

[2048 AI approaches and heuristic (article)](https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf)

