from tree_node import Node


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

        """
        # children of node
        self.children = np.array([])
        # Move made to arrive at node
        self.move = None
        # game object
        clone = game.copy()
        self.game = clone

        # which player's turn it is
        self.player = game.SYMBOLS[game.turn]

        # How many times a child has been expanded.
        self.child_expansions = 0

        # Node stats for UCB calculation
        self.visits = 0
        self.score = 0

        self.populate_children()

    def predicted_move(self):
        """
        Return move from child with highest ucb.

        """
        return self.ucb(c_const=0).move
