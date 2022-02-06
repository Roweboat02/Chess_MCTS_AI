from copy import deepcopy
from collections import deque
from math import log, sqrt

class Node:
    """
    Tree node containg a game state, connected nodes are immediately reachable
    game states.
    """
    def __init__(self, parent, move=None):
        self.game = deepcopy(parent)
        self.move = move
        if move is not None:
            self.game.make_move(move)

        self.visited = False

        self.children = None
        self._unvisited_index = None

        #Node stats for UCB calculation
        self.visits = 0
        self.score = 0

    def populate(self):
        self.visited = True
        self.children = [Node(self.game, move) for move in self.game.possible_moves()]
        self._unvisited_index = len(self.children)

    @property
    def winner(self):
        return self.game.winner

    def increase_or_decrease(self, outcome):
        return 1 if ('X','O')[self.game.turn] == outcome else -1

    @property
    def child(self):
        if self._unvisited_index > 0:
            self._unvisited_index-=1
            return self.children[self._unvisited_index]
        else:
            return self.ucb()

    def ucb(self, c_const=1.41, _print=False):
        """
        Find child in children list with greatest upper confidence bound.
        UCB given by UCB(v,vi) = Q(vi)/N(vi) + c*[ln(N(v))/N(vi)]^1/2
        Where v is current node, vi is child,
        c is an exploitation constant,
        Q() gives score of a node,
        N() gives visits to a node,
        """
        ucb_values = [_child.score / _child.visits + c_const * sqrt( log(self.visits) / _child.visits) for _child in self.children]
        if _print:
            print(ucb_values)
        return children[ucb_values.index(max(ucb_values))]

    def update_score(self, outcome, proximity):
        """
        Backpropogate outcome up path.
        If outcome matches the turn, increase. Else decrease.
        """
        #Each node is visited if it's on the back propogation trail.
        self.visits += 1

        if outcome == 'TIE':
            return
        else:
            a = self.increase_or_decrease(outcome) * (1+(6/proximity**2))
            self.score += self.increase_or_decrease(outcome) * (1+(6/proximity**2))
            return

    def rollout(self, depth):
        """
        Make random moves until terminal state is found.
        Returns
        -------
        outcome
            outcome is item from self.game.SYMBOLS representing winner.
        """
        game = deepcopy(self.game)
        while game.winner is None:
            depth+=1
            game.make_random_move()

        return game.winner, depth