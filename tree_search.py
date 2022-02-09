from tree import Node

class MCTS:

def mcts(node, depth=0):
    depth+=1
    if node.winner is not None:
        result = node.winner

    elif node.visited is False:
        node.populate()
        result, depth = node.rollout(depth)

    else:
        result, depth = mcts(node.child, depth)

    node.update_score(result, depth)
    return result, depth

def find_best_move(game, simulations=200):
    node = Node(game)
    for _ in range(simulations):
        mcts(node)
    return node.ucb(_print=True).move
