# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        visited = []
        leaf = []
        legalMove = state.getLegalPacmanActions()
        record = [(state, state.generatePacmanSuccessor(action), action) for action in legalMove]
        while len(record) != 0:
			path = record.pop(0)
			st = path[1]
			ac = path[2]
			if st.isWin():
				return ac
			else:
				if st not in visited:
					visited.append(st)
        			legal = st.getLegalPacmanActions()
        			for action1 in legal:
        				successors = (st, st.generatePacmanSuccessor(action1), ac)
        				if successors[1] != None:
        					record.append(successors)
        				else:
        					leaf.append((admissibleHeuristic(st), ac))
        	
        best = min(leaf)[0]
        bestActions = [pair[1] for pair in leaf if pair[0] == best]
        return random.choice(bestActions)
        
class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        visited = []
        leaf = []
        legalMove = state.getLegalPacmanActions()
        record = [(state, state.generatePacmanSuccessor(action), action) for action in legalMove]
        while len(record) != 0:
			path = record.pop()
			st = path[1]
			ac = path[2]
			if st.isWin():
				return ac
			else:
				if st not in visited:
					visited.append(st)
        			legal = st.getLegalPacmanActions()
        			for action1 in legal:
        				successors = (st, st.generatePacmanSuccessor(action1), ac)
        				if successors[1] != None:
        					record.append(successors)
        				else:
        					leaf.append((admissibleHeuristic(st), ac))   	
        best = min(leaf)[0]
        bestActions = [pair[1] for pair in leaf if pair[0] == best]
        return random.choice(bestActions)

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        import Queue
        record = Queue.PriorityQueue()
        visited = []
        legalMove = state.getLegalPacmanActions()
        g = 1
        f = (1000, "STOP")
        for action in legalMove:
        	success = state.generatePacmanSuccessor(action)
        	record.put((g + admissibleHeuristic(success), success, action))
        while record.qsize() != 0:
			path = record.get()
			st = path[1]
			ac = path[2]
			g = path[0] - admissibleHeuristic(st)
			if st.isWin():
				return ac
			else:
				if st not in visited:
					visited.append(st)
        			legal = st.getLegalPacmanActions()
        			g += 1
        			for action1 in legal:
        				suc = st.generatePacmanSuccessor(action1)
        				if suc != None:
        					successors = (g + admissibleHeuristic(suc), suc, ac)
        					record.put(successors)
        					if g + admissibleHeuristic(suc) <= f[0]:
        						f = (g + admissibleHeuristic(suc), ac)			   
        return f[1]
