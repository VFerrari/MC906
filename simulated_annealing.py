'''
Project 1 - Search-based solutions for static Pac-Man game.

sa.py: Simulated Annealing search solutions for problem.

Subject:
    MC906/MO416 - Introduction to Artificial Intelligence.
Authors:
    Daniel Helú Prestes de Oliveira - RA 166215
    Eduardo Barros Innarelli        - RA 170161
    Matheus Rotta Alves             - RA 184403
    Victor Ferreira Ferrari         - RA 187890
    Vinícius Couto Espindola        - RA 188115

University of Campinas - UNICAMP - 2020

Last Modified: 01/05/2020.
'''

# This block will allow relative imports from the AIMA folder
# Call it before any other import
import os, sys
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,f'{dir}/aima-python')

import numpy as np
from search import Problem
from search import simulated_annealing_full
# from PacProblemNoMaze import PacProblem
from PacProblemCarryCost import PacProblem

# class PacProblem(Problem):
#     ''' Modeling the static Pac-Man game problem for search. '''
    
#     def __init__(self, initial, goal, maze):
#         ''' Initial State:
#             Tuple of 2 elements. (i,j) in maze.
#             Goal State:
#             Tuple of 2 elements. (i,j) in maze.
#             Maze:
#             NumPy array of BYTES (to save RAM)
#             flags (sa):
#             dictionary with the 
#         '''
#         Problem.__init__(self, initial, goal)
#         self.maze = maze

#     def actions(self, state):
#         ''' A state is the index of the maze (tuple). 
#             An action is a tuple of i,j with the direction to walk.
#         '''
#         self.maze[state] = ' ' # Eat dot

#         actions = []
#         possible = [(1,0),(-1,0),(0,1),(0,-1)]
#         idx = state
#         for action in possible:
#             nxt = list(map(sum, zip(idx,action)))
            
#             # Check circling around maze. If < 0, negative indexing will do the job.
#             if nxt[0] == self.maze.shape[0]:
#                 nxt[0] = 0
#             elif nxt[1] == self.maze.shape[1]:
#                 nxt[1] = 0
#             nxt = tuple(nxt)
            
#             # Check ghosts and walls.
#             if self.maze[nxt] not in [b'o', b'|', b'-']:
#                 actions.append(action)
#         return actions

#     def goal_test(self, state):
#         ''' Check if the Pac-Man reaches its destination.'''
#         return state == self.goal

#     def result(self, state, action):
#         ''' The result of an action is to move to the next position, and eat the point if needed.'''
#         idx = state
        
#         # Get next position.
#         nxt = list(map(sum, zip(idx,action)))
        
#         # Circle around maze. If < 0, negative indexing will do the job.
#         if nxt[0] == self.maze.shape[0]:
#             nxt[0] = 0
#         elif nxt[0] < 0:
#             nxt[0] = self.maze.shape[0]-1
#         elif nxt[1] == self.maze.shape[1]:
#             nxt[1] = 0
#         elif nxt[1] < 0:
#             nxt[1] = self.maze.shape[1]-1
        
#         nxt = tuple(nxt)
#         return nxt
    
#     def path_cost(self, c, state1, action, state2):
#         ''' 10 points if it eats a point, and minus 1 point per movement. '''
#         if self.maze[state2] == b'.':
#             cost = c-10
#         else:
#             cost = c
#         return cost+1

#     # TODO: Supervalue to goal and parameters of the cooling function
#     def value(self, state):
#         ''' Value is the "score" for the state.'''
#         # Use the score as a heuristic
#         # if self.maze[state] == b'.': return 10
#         # else: return 0
        
#         # Use euclidean distance as a heuristic
#         Ax,Ay = state
#         Bx,By = self.goal
#         return -10*np.sqrt((Ax-Bx)**2 + (Ay-By)**2)

#         # Use manhatam distance as a heuristic
#         # Ax,Ay = state
#         # Bx,By = self.goal
#         # return -10*(np.abs(Ax-Bx) + np.abs(Ay-By))

# def get_best_path(path, maze, goal):
#         ''' Calculate the cost after getting a path from some search method. '''
#         min_idx = None 
#         min_cost = sys.maxsize

#         cost = -1
#         for i,p in enumerate(path):        
#             if maze[p] == b'.':
#                 maze[p] = ' ' 
#                 cost -= 10
#             cost += 1 # Pay to move

#             # Check if at a goal state with a better cost
#             if p == goal and cost < min_cost:
#                 min_cost = cost
#                 min_idx = i

#         # Check it reached the goal state at all
#         if min_idx : return (path[:min_idx+1], min_cost)
#         else : None

# NOTE: It assumes the state contains it's respective score
def get_best_path(states, maze, goal):
        ''' Calculate the cost after getting a path from some search method. '''
        min_idx = None 
        min_cost = sys.maxsize

        for i,(p,c) in enumerate(states):        
            # Check if at a goal state with a better cost
            if p == goal and c < min_cost:
                min_cost = c
                min_idx = i

        # Check it reached the goal state at all
        if min_idx: 
            path = [states[i][0] for i in range(min_idx+1)]
            return True, (path, min_cost)
        else: 
            path = [s[0] for s in states]
            return False, (path, None)

def cooling_func(k=10, lam=0.001, limit=2000):
    """One possible schedule function for simulated annealing"""
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0)

def sa_pacman(maze, fill=False, wrong_path=True):
    # Get maze from file
    if fill: maze[maze==b' '] = b'.'

    # Get and clear positions
    init = tuple(map(int, np.where(maze==b'!')))
    goal = tuple(map(int, np.where(maze==b'?'))) 
    maze[init] = b' '
    maze[goal] = b' '

    # Copy for post processing
    maze_ref = maze.copy() 
    
    # Create Problem
    prob = PacProblem((init,0), goal, maze) # Add initial cost 0 with init
    assert maze[goal] == b'.' or maze[goal] == b' ', "Goal unreachable."
    
    # Solve with Simulated Annealing
    states = simulated_annealing_full(prob, schedule=cooling_func())

    # Get the best path found
    reached,best = get_best_path(states, maze_ref, goal)
    if not reached: print("The search failed to reach a final state.")
    
    # If goal reached return best
    if reached:
        return best
    # If wrong path allowd, return it since did not reach
    elif wrong_path:    
        return best

if __name__ == '__main__':
    maze_file = 'mazes/dense/1a'
    maze = np.genfromtxt(maze_file, dtype=str, delimiter=1).astype('bytes')
    best = sa_pacman(maze)
    if best:
        print('\nAcquired Path: \n', best)
    else:
        print('\nThe goal was never reached.')