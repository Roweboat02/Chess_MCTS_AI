from __future__ import annotations

import random
from copy import deepcopy
from math import log, sqrt
import fog_of_war_chess as fow

class Node:
    """
    Tree node containg a game state, connected nodes are immediately reachable
    game states.
    """
    def __init__(self, game:fow.FOWChess, depth:int, move:str=None) -> None:
        self.game = deepcopy(game)
        self.move = move
        if move is not None:
            self.game.make_move(move)
        self.depth = depth

        self.visited = False

        self.is_terminal = False

        self.children = None
        self._unvisited_list = None

        #Node stats for UCB calculation
        self.visits = 0
        self.score = 0

    def populate(self) -> None:
        self.visited = True
        self.children = [Node(self.game, move) for move in self.game.possible_moves()]
        self._unvisited_list = self.children.copy()


    @property
    def child(self) -> Node:
        if self._unvisited_list:
            return self._unvisited_list.pop(random.randint(0, len(self._unvisited_list)))
        else:
            return self.ucb()

    def ucb(self, c_const:float=1.41, _print:bool=False) -> Node:
        """
        Find child in children list with the greatest upper confidence bound.
        UCB given by UCB(v,vi) = Q(vi)/N(vi) + c*[ln(N(v))/N(vi)]^1/2
        Where v is current node, vi is child,
        c is an exploitation constant,
        Q() gives score of a node,
        N() gives visits to a node,
        """
        ucb_values = [_child.score / _child.visits + c_const * sqrt( log(self.visits) / _child.visits) for _child in self.children]
        if _print:
            print(ucb_values)
        return self.children[ucb_values.index(max(ucb_values))]

    def update_score(self, score_change:int) -> None:
        """
        Backpropogate outcome up path.
        If outcome matches the turn, increase. Else decrease.
        """
        #Each node is visited if it's on the back propogation trail.
        self.visits += 1
        self.score += score_change

    def rollout(self, depth:int):
        """
        Make random moves until terminal state is found.
        Returns
        -------
        outcome
            outcome is item from self.game.SYMBOLS representing winner.
        """
        game = deepcopy(self.game)
        while self.is_terminal is False:
            depth+=1
            game.make_random_move()

        return game.winner, depth
