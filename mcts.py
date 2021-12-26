import time

"""
INCOMPLETE!
"""



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
    # Determine if node is terminal
    if node.has_winner():
        outcome, immediate = node.game.winner, True
    else:
        if (not node.has_children()) or node.has_unvisited_children():
            # If there are unexpanded children, choose one randomly
            child = node.child_expansion()
            outcome, immediate = child.rollout()
            child.update_score(outcome, immediate)

        else:
            # If all are expanded, pick child with greatest UCB
            outcome, immediate = recursive_tree_search(node.ucb())

    # Back propogate by returning outcome and recursively updating values.
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
    while time.time() - start < durration:
        # for i in range (500):
        recursive_tree_search(root)
    return root.predicted_move()
