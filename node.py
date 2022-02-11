from __future__ import annotations

import random
from typing import List, Dict

import fog_of_war_chess as fow
import move as mv


class Node:
    """
    Tree node containg a game state, connected nodes are immediately reachable
    game states.
    """
    def __init__(self, game:fow.FOWChess, depth:int, move:mv.Move) -> None:
        self.game: fow.FOWChess = game
        self.depth: int = depth
        self.move: mv.Move = move

        self.visited: bool = False

        self.possible_moves: List[mv.Move] = []
        self.children: List[Node] = []
        self._unvisited_list: List[Node] = []

        #Node stats for UCB calculation
        self.visits: int = 0
        self.score: int = 0

    def populate(self) -> None:
        self.visited = True
        self.possible_moves = self.game.possible_moves()
        self.children = [Node(self.game.make_move(move), self.depth+1, move) for move in self.possible_moves]
        self._unvisited_list = self.children.copy()

    def update_score(self, score_change:int) -> None:
        """
        Backpropogate outcome up path.
        If outcome matches the turn, increase. Else decrease.
        """
        #Each node is visited if it's on the back propogation trail.
        self.visits += 1
        self.score += score_change
