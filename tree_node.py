import random
import numpy as np


class Node:
    """
    Tree node containg a game state, connected nodes are immediately reachable
    game states.
    """

    def __init__(self, game, move=None):
        """
        Node for game state.
        See module docsting for game requirements.

        Parameters
        ----------
        parent
            An object representing a game. See module docsting for requirements.
        move
            None if root

        """
        self.children = None
        self.game_state = game
        self.move = move

        # Node stats for UCB calculation
        self.visits = 0
        self.score = 0

    @classmethod
    def from_game(): pass

    @classmethod
    def child_from_self(): pass

    def populate_children(self):
        """
        Expand a given node by finding and populating children array
        with all possible next game states.

        """
        self.children = [Node.child_from_self(self, move=move) for move in self.game.legal_moves]

    def has_unvisited_children(self):
        """
        If a child in children has visits=0, return True.

        """
        return len(self.children) > self.child_expansions

    def has_visited_children(self):
        """
        If a child in children has visits!=0, return True.

        """
        return self.child_expansions > 0

    def has_children(self):
        """
        If children array is populated, return True
        """
        return self.children.size > 0

    def ucb(self, c_const=1.41):
        """
        Find child in children list with greatest upper confidence bound.
        UCB given by UCB(v,vi) = Q(vi)/N(vi) + c*[ln(N(v))/N(vi)]^1/2
        Where v is current node, vi is child,
        c is an exploitation constant,
        Q() gives score of a node,
        N() gives visits to a node,


        Parameters
        ----------
        c_const : TYPE, optional
            DESCRIPTION. The default is 1.41.

        Returns
        -------
        Node
            Node form children that generates max UCB.

        """

        ucb_values = [(child.score / child.visits) +
                      c_const * np.sqrt(np.log(self.visits) / child.visits)
                      for child in self.children]
        return self.children[np.argmax(ucb_values)]

    def update_score(self, outcome, immediate):
        """
        Backpropogate the outcome up path.
        If outcome matches self.player, increase. Else decrease.

        Parameters
        ----------
        immediate
            An additional penalty for closeness to the losing position.
        outcome
            Outcome is item from self.game.SYMBOLS representing winner.

        """
        # Each node is visited if it's on the back propogation trail.
        self.visits += 1

        if outcome == 'tie':
            return
        if self.player == outcome:
            self.score += 1
        else:
            self.score -= (1 + 9999 * immediate)

    def rollout(self):
        """
        Make random moves until terminal state is found.

        Returns
        -------
        outcome
            outcome is item from self.game.SYMBOLS representing winner.

        """
        if self.has_winner():
            return self.game.winner, True
        simulation_copy = self.game.copy()
        while simulation_copy.winner is None:
            simulation_copy.make_random_move()
        return simulation_copy.winner, False

    def has_winner(self):
        """
        Simple method to determine if winner is something other than None.

        Returns
        -------
        bool

        """
        return self.game.has_winner()

    def child_expansion(self):
        """
        Choose a child randomly, expand it and return it.

        Returns
        -------
        child : Node
            Expanded node from self.children.

        """
        self.child_expansions += 1
        child = random.choice([child for child in self.children if child.visits == 0])
        # Expand
        child.populate_children()
        return child
