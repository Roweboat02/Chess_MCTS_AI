# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 17:48:52 2021

@author: noahr


Created on Sun Aug 15 16:43:31 2021

@author: noahr

Monte carlo tree search class and functions.
A game needs to have:
    Class attributes:
    SYMBOLS : iterable
        SYMBOLS Should include all differentiations between players.
        Is never used stricly as a class attribute, but must be constant.

    Object attributes:
    turn : obj from SYMBOLS (i.e. int, str, ect.)
        an object belonging to SYMBOLS which is used to denote which player
        is expected to make an action.
    winner : obj from SYMBOLS (i.e. int, str, ect.)
        an object belonging to SYMBOLS which is used to denote which player
        has won. Winner should be updated by game class after a state change.
    Methods:
    next_moves_list()
        Returns a list or array of all reachable states immediately after the current game state.
    copy()
        Returns an identical, entirely independant copy of the game in it's current state.
    make_move(move)
        Change from current game state to state described with move param.
    make_random_move()
        Change from current game state to an immediately reachable randomly selected state.
"""

import random
import time
import numpy as np

class Node:
    """
    Tree node containg a game state, connected nodes are immediately reachable
    game states.
    """
    def __init__(self, parent, move=None):
        """
        Node for game state.
        See module docsting for game requirements.

        Parameters
        ----------
        game
            An object representing a game. See module docsting for requirements.
        move
            None if root

        """
        #children of node
        self.children = np.array([])
        #Move made to arrive at node
        self.move = move
        #game object
        clone = parent.game.copy()
        clone.make_move(move)
        self.game = clone

        #How many time a child has been expanded.
        self.child_expansions = 0

        #which player's turn it is
        self.player = parent.player

        #Node stats for UCB calculation
        self.visits = 0
        self.score = 0

    def populate_children(self):
        """
        Expand a given node by finding and populating children array
        with all possible next game states.

        """
        self.children = np.array([Node(self, move=move) for move in self.game.legal_moves])

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
        exploit_const : TYPE, optional
            DESCRIPTION. The default is 1.41.

        Returns
        -------
        Node
            Node form children that generates max UCB.

        """

        ucb_values = [(child.score/child.visits)+
                      c_const*np.sqrt(np.log(self.visits)/child.visits)
                      for child in self.children]
        return self.children[np.argmax(ucb_values)]

    def update_score(self, outcome, immediate):
        """
        Backpropogate outcome up path.
        If outcome matches self.player, increase. Else decrease.

        Parameters
        ----------
        outcome
            outcome is item from self.game.SYMBOLS representing winner.

        """
        #Each node is visited if it's on the back propogation trail.
        self.visits += 1

        if outcome == 'tie':
            return
        if self.player == outcome:
            self.score+=1
        else:
            self.score-=(1+9999*immediate)

    def rollout(self):
        """
        Make random moves until terminal state is found.

        Returns
        -------
        outcome
            outcome is item from self.game.SYMBOLS representing winner.

        """
        if self.has_winner():
            return (self.game.winner,True)
        simulation_copy = self.game.copy()
        while simulation_copy.winner is None:
            simulation_copy.make_random_move()
        return (simulation_copy.winner,False)

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
        self.child_expansions+=1
        child = random.choice([child for child in self.children if child.visits == 0])
        #Expand
        child.populate_children()
        return child

class Root(Node):
    """
    Node generated from a game state instead of another Node.
    """
    def __init__(self, game):
        """
        Node for game state.
        See module docsting for game requirements.

        Parameters
        ----------
        game
            An object representing a game. See module docsting for requirements.
        move
            None if root

        """
        #children of node
        self.children = np.array([])
        #Move made to arrive at node
        self.move = None
        #game object
        clone = game.copy()
        self.game = clone

        #which player's turn it is
        self.player = game.SYMBOLS[game.turn]

        #How many times a child has been expanded.
        self.child_expansions = 0

        #Node stats for UCB calculation
        self.visits = 0
        self.score = 0

        self.populate_children()

    def predicted_move(self):
        """
        Return move from child with highest ucb.

        """
        return self.ucb(c_const=0).move

def recursive_tree_search(node):
    """
    Recursive monte carlo tree search.

    Parameters
    ----------
    node : Node
        A tree node describing gamestate.

    Returns
    -------
    outcome
        outcome is item from self.game.SYMBOLS representing winner.

    """
    #Determine if node is terminal
    if node.has_winner():
        outcome, immediate = (node.game.winner,True)
    else:
        if (not node.has_children()) or node.has_unvisited_children():
            #If there are unexpanded children, choose one randomly
            child = node.child_expansion()
            outcome, immediate = child.rollout()
            child.update_score(outcome, immediate)

        else:
            #If all are expanded, pick child with greatest UCB
            outcome, immediate = recursive_tree_search(node.ucb())

    #Back propogate by returning outcome and recursively updating values.
    node.update_score(outcome, immediate)
    return outcome, immediate

def mcts(game, durration=0.5):
    """
    Monte carlo tree search.

    Parameters
    ----------
    game
        The game state a move is searching from.
    durration : float
        Time in seconds MCTS persists. The default is 0.5.

    Returns
    -------
        Best discovered move.

    """
    root = Root(game)

    start = time.time()
    while time.time()-start<durration:
    # for i in range (500):
        recursive_tree_search(root)
    print([(child.score,child.visits) for child in root.children])
    print([child.score/child.visits for child in root.children])
    return root.predicted_move()
