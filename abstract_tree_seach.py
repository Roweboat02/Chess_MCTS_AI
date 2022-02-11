from abc import ABC, abstractmethod
from math import sqrt, log
import random

from fog_of_war_chess import FOWChess
from node import Node


class AbstractTreeSearch(ABC):

    @abstractmethod
    def is_terminal_state(self, state:FOWChess, depth:int)-> bool: pass

    @abstractmethod
    def terminal_state_value(self, state:FOWChess, depth:int) -> int: pass

    @abstractmethod
    def update_node_score(self, node:Node, result:int) -> None: pass

    def ucb(self, node:Node, c_const:float=1.41,) -> Node:
        """
        Find child in children list with the greatest upper confidence bound.
        UCB given by UCB(v,vi) = Q(vi)/N(vi) + c*[ln(N(v))/N(vi)]^1/2
        Where v is current node, vi is child,
        c is an exploitation constant,
        Q() gives score of a node,
        N() gives visits to a node,
        """
        ucb_values = [_child.score / _child.visits + c_const * sqrt( log(node.visits) / _child.visits)
                      for _child in node.children]
        return node.children[ucb_values.index(max(ucb_values))]

    def best_child(self, node: Node) -> Node:
        if node._unvisited_list:
            return node._unvisited_list.pop(random.randint(0, len(node._unvisited_list)))
        else:
            return self.ucb(node)

    def rollout(self, node:Node, depth:int)-> int:
        """
        Make random moves until terminal state is found.
        Returns
        """
        game:FOWChess = node.game
        while not self.is_terminal_state(game, depth):
            game = game.make_random_move()
            depth+=1
        return self.terminal_state_value(game, depth)

    def mcts(self, node:Node, depth:int=0)-> int:
        if self.is_terminal_state(node.game, depth):
            result:int = self.terminal_state_value(node.game, depth)

        elif not node.visited:
            node.populate()
            result:int = self.rollout(node, depth)

        else:
            result:int = self.mcts(self.best_child(node), depth+1)

        self.update_node_score(node, result)

        return result

    @abstractmethod
    def simulate(self, game:FOWChess, simulations:int=200)-> Node: pass
