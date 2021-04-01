# Tic Tac Toe

	__|__|__
	__|__|__
	  |  |

Installation instructions:

1. Make sure you have <a href="https://www.python.org/downloads/">Python</a> 3.x installed on your machine.

2. Make sure you have the <a href="https://www.pygame.org/wiki/GettingStarted">PyGame</a> library installed.

3. Run the tictac.py script.

About:

This is an implementation of Tic Tac Toe using the PyGame GUI.

The user plays against the computer in this version of Tic Tac Toe. Using a combination of the minimax algorithm and a Tree data structure, the computer looks for the best move to play where it maximizes its
chances of winning based on the premise that the user will play the most optimal move. If the computer cannot win, it will make sure to drag the game
 to a point of draw. This is done by making sure that the outcome is dependent on how deep the computer searches for a move. 

There are controls to reset or quit the game. There is a scorecard which keeps track of the score for each active session.
