# Chess_MCTS_AI

## Intro
This project is an attempt at making a system for training a neural network from self-play, to play an asymmetric information game, tabula rasa.
(essentially just means a neural network that learns everything about a game where players can have different amounts of information about the game state, by playing the game and learning based on if it wins or loses.)

The asymmetric game used is the fog of war (FOW) variant of chess.
https://www.chess.com/terms/fog-of-war-chess

The design used is loosely based on different iterations of the Google DeepMind team's chess and go AI's.


## Project plan:
An implementation of the *Monte Carlo search tree* algorithm using a complete game state (no information is obscured) is used to map and evaluate possible moves via random simulation.

The neural network will take as an input:
- The sequence of all past moves made by a player
- A representation of the current game state
- A vector of possible moves

The input will use the imperfect (information is obscured) representations of the game. In FOW, this means the fog of the current board is applied to the board representation. Each potential move will be represented as the current board with it's fog applied, where the piece to be moved will be placed at it's destination square **WITHOUT** updating the fog from the parent state.

The neural network will process the sequence of past moves using a recurrent neural network architecture to help emphasize the sequential nature of the data. The current game state after passing through a series of resnet blocks will be combined the the output derived from the sequence of past moves, before passing through more convolutional layers.

The network is expected to output a probability distribution across the given set of moves. This data can be at first corrected using results from the mcts network, until an experimental point in training is reached. At this point, the mcts will be discarded and the network's win-loss ratio can be used going forwards.
