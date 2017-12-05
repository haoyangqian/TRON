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
        return alpha_beta_cutoff(asp,1,self.heur)
        
    def sigmoid(self,x):
        #a function that maps any real number to a value between 0 and 1
        return 1 / (1 + math.exp(-x))
        
    def manhattan_distance(self,dst,src):
        return abs(dst[0] - src[0]) + abs(dst[1] - src[1])

    def heur(self,state):
        origin = state.player_locs[self.player]
        opponent = state.player_locs[(self.player+1)%2]
        score, connected = self.bfs_with_powerup(state,self.player)
        #scale score down so the sigmoid function is more responsive
        if not connected:
            #print "not connected"
            return self.sigmoid(score/200.0)
        else:
            # if connected, try to get close to opponent
            #print "connected"
            # score1, score2 = self.calculateScore(state,self.player)
            # print score1, score2
            # return self.sigmoid((score1 - score2)/200.0)
            return -self.manhattan_distance(origin, opponent)

    def bfs_with_powerup(self,state,play_num): #a bounded search of how many tiles are accessible
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
                if self.manhattan_distance(curr, opponent) == 1:
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

    def bfs(self,state,play_num): #a bounded search of how many tiles are accessible
        board = state.board
        origin = state.player_locs[play_num]
        opponent = state.player_locs[(play_num+1)%2]
        visited = set()
        Q = Queue.Queue()
        Q.put(origin)
        visited.add(origin)
        #print state.board
        while not Q.empty():
            size = Q.qsize()
            for i in range(size):
                curr = Q.get()
                valid_moves = list(TronProblem.get_safe_actions(board,curr))
                for direction in valid_moves:
                    neighbor = TronProblem.move(curr,direction)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        Q.put(neighbor)
        score = len(visited)
        #print score
        return score

    def calculateScore(self, state, play_num):
        board = state.board
        score1, score2 = 0, 0
        origin = state.player_locs[play_num]
        opponent = state.player_locs[(play_num+1)%2]
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ' ' or board[i][j] == '*':
                    dis1 = self.manhattan_distance(origin, (i,j))
                    dis2 = self.manhattan_distance(opponent, (i,j))
                    if dis1 > dis2:
                        score1 += 1
                    elif dis2 > dis1:
                        score2 += 1
        return score1, score2

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
