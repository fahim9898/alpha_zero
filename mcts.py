import numpy as np
import copy
# import game


def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs

class TreeNode():
    def __init__(self , parent , prior_p):
        self._parent = parent
        self._Q = 0
        self._n_visit = 0
        self._children = {}
        self._p = prior_p

    def is_root_node(self):
        return (True if self._parent == None else False)

    def is_leaf(self):
        return (True if len(self._children) == 0 else False )
    
    def get_values(self , c_put):

        U = c_put * self._p * np.sqrt(self._parent._n_visit) /(1+self._n_visit)
        Q = self._Q
        return Q + U 
    
    def select(self , c_put):

        """
            Select greedy action when current node is not leaf node 
            MAX(Q + Upper confidence value)

        """
        return max(self._children.items() , key= lambda act_node: act_node[1].get_values(c_put)) 
        # random(self._Q + self._p/self._n_visit )
    
    def expand_node(self , action_prob):
        for action , prob in action_prob:
            if action in self._children:
                print("**********************************************************************")
            if action not in self._children:
                self._children[action] = TreeNode(self , prob)
        # print("expand done")
    
    def update(self , leaf_value ):
        self._n_visit += 1
        # print("!" , end="")
        self._Q +=  (leaf_value - self._Q) / self._n_visit
    # def _playout(self):
        
    def update_recursive(self , leaf_value):

        if self._parent:
            self._parent.update_recursive(-leaf_value)   # Minius sign indicate alternate between two player 

        self.update(leaf_value)
    
    # def update_with_move(self.)

class MCTS:
    def __init__(self , policy, n_playout , c_put):
        self._policy = policy
        self.root_node = TreeNode(None , 1.0)
        self.n_playout = n_playout
        self.c_put = c_put

    def _playout(self , state):
        node = self.root_node
        while(1):
            if node.is_leaf():
                break
            else:
                action , node = node.select(self.c_put)
                state.do_move(action)

        prob , leaf_value = self._policy(state)
        win , winner = state.end_game(1)

        if not win:
            # print("+" , end="")
            node.expand_node(prob)
        else:
            if winner == -1:
                leaf_value = 0.0
            else:
                leaf_value = 1.0 if winner == state.get_current_player() else -1.0

        node.update_recursive(-leaf_value)

    def get_move_probability(self , state , temp = 1e-3):
        for n in range(self.n_playout):
            copy_state = copy.deepcopy(state)
            self._playout(copy_state)
            # print("-")
        
        act_visits= [(act , node._n_visit)
                        for act,node in self.root_node._children.items() ]
        # print(act_visits , "++++" , self.root_node._children.items())
        print(act_visits)
        acts , visits = zip(*act_visits)

        action_prob = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))


        return acts , action_prob
    

    def update_root_node(self , last_move):
        if last_move in self.root_node._children:
            self.root_node = self.root_node._children[last_move]
            self.root_node._parent = None
        else:
            self.root_node = TreeNode(None, 1.0)


class MCTS_Player:
    def __init__(self , policy , c_put= 5 , n_playout=2000 , _is_selfplay = 0):

        self.mcts = MCTS(policy , n_playout , c_put)
        self._is_selfplay = _is_selfplay
    
    def reset_player(self):
        self.mcts.update_root_node(-1)

    def get_action(self , board , temp = 1e-3 , return_prob = 0):
        sensible_moves = board.available_state
        # print(sensible_moves)
        move_prob = np.zeros(board.width*board.height)
        if len(sensible_moves) > 0:
            acts , probs = self.mcts.get_move_probability(board , temp)
            # print("okay in")
            move_prob[list(acts)] = probs

            if self._is_selfplay:
                move = np.random.choice(
                    acts,
                    p=0.75*probs + 0.25 *
                    np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                print("------" , move,"-------")
                # update the root node and reuse the search tree
                self.mcts.update_root_node(move)
            else:
                # to choosing the move with the highest prob
                move = np.random.choice(acts, p=probs)
                # reset the root node
                self.mcts.update_root_node(-1)

            if return_prob:
                return move , move_prob
            else:
                return move
        else:
            print("WARNING : board is full")

""" 
class MCTS:
    "In class all MCTS function work example intial node , playout return probability for training and "

    def __init__():
    def _playout():
    def get_move_probability():
    def update_with_move():

class MCTS_Player:
    def __init__():
    def reset_tree():
    def get_action(): 
        
"""
