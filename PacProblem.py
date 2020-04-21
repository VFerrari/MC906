'''
Project 1 - Search-based solutions for static Pac-Man game.

PacProblem.py: Basic problem type for Pac-Man problem.

Subject:
    MC906/MO416 - Introduction to Artificial Intelligence.
Authors:
    Daniel Helú Prestes de Oliveira - RA 166215
    Eduardo Barros Innarelli        - RA 170161
    Matheus Rotta Alves             - RA 184403
    Victor Ferreira Ferrari         - RA 187890
    Vinícius Couto Espindola        - RA 188115

University of Campinas - UNICAMP - 2020

Last Modified: 20/04/2020.
'''

from search import Problem

class PacProblem(Problem):
    ''' Modeling the static Pac-Man game problem for search. '''
    
    def __init__(self, initial, goal):
        ''' Initial State:
            Tuple of 2 elements. 1-Initial maze. 2. (i,j) in maze.
            Goal State:
            Tuple of 2 elements. (i,j) in maze.
            Maze:
            NumPy array of BYTES (to save RAM)
        '''
        Problem.__init__(self, initial, goal)
        
    def actions(self, state):
        ''' A state is the current maze (NumPy 2D array) and the index of the maze (tuple). 
            An action is a tuple of i,j with the direction to walk.
        '''
        actions = []
        possible = [(1,0),(-1,0),(0,1),(0,-1)]
        maze,idx = state
        for action in possible:
            nxt = list(map(sum, zip(idx,action)))
            
            # Check circling around maze. If < 0, negative indexing will do the job.
            if nxt[0] == maze.shape[0]:
                nxt[0] = 0
            elif nxt[1] == maze.shape[1]:
                nxt[1] = 0
            nxt = tuple(nxt)
            
            # Check ghosts and walls.
            if maze[nxt] != b'O' and maze[nxt] != b'|' and maze[nxt] != b'-':
                actions.append(action)
        return actions

    def goal_test(self, state):
        ''' Check if the Pac-Man reaches its destination.'''
        return state[1] == self.goal

    def result(self, state, action):
        ''' The result of an action is to move to the next position, and eat the point if needed.'''
        maze, idx = state
        
        # Get next position.
        nxt = list(map(sum, zip(idx,action)))
        
        # Circle around maze. If < 0, negative indexing will do the job.
        if nxt[0] == maze.shape[0]:
            nxt[0] = 0
        elif nxt[0] < 0:
            nxt[0] = maze.shape[0]-1
        elif nxt[1] == maze.shape[1]:
            nxt[1] = 0
        elif nxt[1] < 0:
            nxt[1] = maze.shape[1]-1
        
        nxt = tuple(nxt)
        
        # Eat point if needed
        next_maze = maze.copy()
        if next_maze[nxt] == b'.': next_maze[nxt] = b' '
        return next_maze,nxt
    
    def path_cost(self, c, state1, action, state2):
        ''' 10 points if it eats a point, and minus 1 point per movement. '''
        if state1[0][state2[1]] == b'.':
            cost = c-10
        else:
            cost = c
        return cost+1

    def value(self, state):
        ''' Value is the "score" for the state.'''
        return -1 * self.path_cost(None, None, None, state)

