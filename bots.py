#!/usr/bin/python

import numpy as np
from tronproblem import TronProblem
import random, Queue, math
from implemented_adversarial import alpha_beta_cutoff


class StudentBot():
    """ Write your student bot here"""
    def decide(self,asp):
        start = asp.get_start_state()
        self.player = start.player_to_move()
        self.board = start.board
        return alpha_beta_cutoff(asp,3,self.heur)
        
    def sigmoid(self,x):
        #a function that maps any real number to a value between 0 and 1
        return 1 / (1 + math.exp(-x))
        
    def manhattan_distance(self,dst,src):
        return abs(dst[0] - src[0]) + abs(dst[1] - src[1])

    def heur(self,state):
        origin = state.player_locs[self.player]
        opponent = state.player_locs[(self.player+1)%2]
        score, connected = self.bfs(state,self.player)
        #scale score down so the sigmoid function is more responsive
        if not connected:
            return self.sigmoid(score/200.0)
        else:
            # if connected, try to get close to opponent
            return -self.manhattan_distance(origin, opponent)
    
    def adjacent(self,a,b):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) <= 1:
            return True
        return False

    def bfs(self,state,play_num): #a bounded search of how many tiles are accessible
        board = state.board
        origin = state.player_locs[play_num]
        opponent = state.player_locs[(play_num+1)%2]
        connected = False
        visited = set()
        Q = Queue.Queue()
        Q.put(origin)
        visited.add(origin)
        level = 0
        powerup = 0
        #print state.board
        while not Q.empty():
            size = Q.qsize()
            level += 1
            for i in range(size):
                curr = Q.get()
                i,j = curr
                #print (i,j)
                if self.board[i][j] == '*':
                    #print (i,j),origin
                    powerup += 10*math.exp(-level)
                if self.adjacent(curr, opponent):
                    connected = True
                valid_moves = list(TronProblem.get_safe_actions(board,curr))
                for direction in valid_moves:
                    neighbor = TronProblem.move(curr,direction)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        Q.put(neighbor)
        score = len(visited) + powerup
        #print score
        return score,connected

    def cleanup(self):
        pass


class RandBot():
    """Moves in a random (safe) direction"""
    def decide(self,asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board,loc))
        if possibilities:
            return random.choice(possibilities)
        return 'U'

    def cleanup(self):
        pass


class WallBot():
    """Hugs the wall"""
    def __init__(self):
        order = ['U','D','L','R']
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ['U','D','L','R']
        random.shuffle(order)
        self.order = order
        
    def decide(self,asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board,loc))
        if not possibilities:
            return 'U'
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board,next_loc)) < 3:
                decision = move
                break
        return decision


class TABot1():
    """a bot that tries to leave itself as much space as possible"""
    def decide(self,asp):
        start = asp.get_start_state()
        self.player = start.player_to_move()
        return alpha_beta_cutoff(asp,3,self.heur)
        
    def sigmoid(self,x):
        #a function that maps any real number to a value between 0 and 1
        return 1 / (1 + math.exp(-x))
        
    def heur(self,state):
        score = self.bfs(state,self.player)
        #scale score down so the sigmoid function is more responsive
        return self.sigmoid(score/200.0)
        
    def bfs(self,state,play_num): #a bounded search of how many tiles are accessible
        board = state.board
        origin = state.player_locs[play_num]
        visited = set()
        Q = Queue.Queue()
        Q.put(origin)
        visited.add(origin)
        while not Q.empty():
            curr = Q.get()
            valid_moves = list(TronProblem.get_safe_actions(board,curr))
            for direction in valid_moves:
                neighbor = TronProblem.move(curr,direction)
                if neighbor not in visited:
                    visited.add(neighbor)
                    Q.put(neighbor)
        return len(visited)

    def cleanup(self):
        pass
