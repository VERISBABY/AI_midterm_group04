# AI_midterm_group04
This is the midterm assignment solutions of course: Introduction to Artificial Intelligence of group 04

*University*: Ton Duc Thang

*Members*:
+ Nguyễn Thị Quế Châu do Task 1
+ Benedict Timothy Chibuike do Task 2
+ Trần Thị Thế Nhân do Task 3

*Task 1: A* with 8-Puzzle*

In the 8-puzzle game, you have to move tiles, given an initial state, to obtain one 
goal state. Note that
• The initial state can be arbitrary permutation of 8 tiles and the blank cell.
• After a move
o If cell 1 and cell 3 are adjacent to each other, horizontally or vertically, 
they are automatically swapped.
o Similar for cell 2 and cell 4.
Students conduct the following requirements:
• Formulate the given problem in form of a state space, determine details of related 
components.
• A* algorithms to solve the game with 02 heuristic functions, explain 
admissibility and consistency of each function.
• Provide a function to illustrate the search tree with n nodes, n is a parameter.
• Propose an experiment to evaluate the optimality of the two selected heuristic.
o Hint: randomize initial state, run the algorithm, measure the average path 
cost of the solution.
• Students organize the program regarding to the OOP model, ensure source code 
is compact and reasonable.

**Task 2: A* with Pacman*

Students implement search strategies to help the pacman to collect all food points in 
the maze.
• Formulate the given problem in form of a state space, determine details of related 
components.
• Implement the A* algorithms to solve the problem, discuss the admissibility and 
consistency of the selected heuristic.
• Implement a complete program to execute designated algorithms, in which
o Input: path to a layout file
o Output: list of actions (North, East, West, South, Stop); total cost
o The maze structure is as below
§ % à obstacles/walls
§ P à initial location of the pacman
§ . à food points, there could be multiple points
§ O à magical pies, pacman can go through walls for the 5 steps 
after eating a pie.
§ spaces à blank cells.
§ There are no ghosts in the maze.
§ If the pacman reaches to a corner, then it automatically teleports to 
the opposite corner of the maze.

o Visualization: students visualize game steps on the console screen (press 
a key to start animation, do not need to press Enter for each step). Students 
are highly recommended to use the pygame library (0.5 bonus points).
• Students organize the program regarding to the OOP model, ensure source code 
is compact and reasonable.
• Recommended editor: Visual Studio Code

*Task 3: 16-queens*

The problem is to place 16 queens on a chess board 16 x 16 so that there is no pair 
of them attacking each other.
Students formulate the game in form of a local search problem and implement a 
genetic algorithm to solve it, in which:
• The crossover step occurs at two random points.
• Mutation ration is flexible, in which the user can specify its value when execute 
the algorithm.
