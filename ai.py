from __future__ import absolute_import, division, print_function
import copy, random

from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0

# AI agent. Determine the next move.
class AI:
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)
        
        # weight matrix
        self.weights = []
        board_size = len(root_state[0])
        for i in range(board_size):
            row = []
            for j in range(board_size):
                power_val = 2*(board_size-1)-j-i
                row.append(4**power_val)
            self.weights.append(row)

    def build_tree(self, node = None, depth = 0):
        #base case
        if depth <= 0 or node is None:
            return
        
        if node.player_type == MAX_PLAYER:
            for direction in MOVES:
                self.simulator.set_state(node.state[0], node.state[1])
                
                # check the validity of moving in the direction
                if self.simulator.move(direction):
                    child = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    self.build_tree(child, depth - 1)
                    node.children.append((direction, child))
                    
        elif node.player_type == CHANCE_PLAYER:
            self.simulator.set_state(node.state[0], node.state[1])
            open_tiles = self.simulator.get_open_tiles()
            for (i, j) in open_tiles:
                
                #manually place a 2 tile
                node.state[0][i][j] = 2
                child = Node(node.state, MAX_PLAYER)
                
                #recursively build tree
                self.build_tree(child, depth - 1)
                
                node.children.append(child)
                node.state[0][i][j] = 0

    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):        
        if node.is_terminal():
            return None, node.state[1]
        elif node.player_type == MAX_PLAYER:
            value = None
            best_direction = None
            for direction, child in node.children:
                _, expectimax_value = self.expectimax(child)
                if value is None:
                    value = expectimax_value
                    best_direction = direction
                elif value < expectimax_value:
                    value = expectimax_value
                    best_direction = direction
            return best_direction, value
        elif node.player_type == CHANCE_PLAYER:
            value = 0 
            count = len(node.children)
            for child in node.children:
                _, expectimax_value = self.expectimax(child)
                value = value + expectimax_value / count
            return None, value
    
    def cal_weights(self, node):
        matrix = node.state[0]
        w = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                w = w + matrix[i][j] * self.weights[i][j]
        return w      
                
    def cal_merges(self, node):
        matrix = node.state[0]
        merges = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)-1):
                if matrix[i][j] == matrix[i][j+1]:
                    merges = merges + 1
                if matrix[j][i] == matrix[j+1][i]:
                    merges = merges + 1
        return merges
    
    # expectimax
    def expectimax_ec(self, node = None):        
        if node.is_terminal():
            old_state = self.simulator.current_state()
            self.simulator.set_state(node.state[0], node.state[1])
            length = len(self.simulator.get_open_tiles())
            self.simulator.set_state(old_state[0], old_state[1])
            return None, 4 + node.state[1] + self.cal_weights(node) + length**4 + self.cal_merges(node)**4
        elif node.player_type == MAX_PLAYER:
            value = None
            best_direction = None
            for direction, child in node.children:
                _, expectimax_value = self.expectimax_ec(child)
                if value is None:
                    value = expectimax_value
                    best_direction = direction
                elif value < expectimax_value:
                    value = expectimax_value
                    best_direction = direction
            return best_direction, value
        
        elif node.player_type == CHANCE_PLAYER:
            value = 0 
            count = len(node.children)
            for child in node.children:
                _, expectimax_value = self.expectimax_ec(child)
                value = value + ( expectimax_value ) / count
            return None, value

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # extra credits
    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax_ec(self.root)
        return direction

