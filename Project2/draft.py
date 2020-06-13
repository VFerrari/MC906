# Since the fitness values are far to close to eachother, 
# the chosen selection methods to handle the mating was
# the rank selection as well as the tournament selection
# since these work well with idividual with near identical
# fitness values. These will also behave well in case we
# choose fitness functions which can have negative values.

from random import sample 
from numpy.random import choice # This name might be taken
import numpy as np

def tournament(self, k, qnt_pairs, no_repeat):
    pool = list(range(len(self.population)))
    winners = []

    for i in range(2*qnt_pairs):
        competitors = sample(pool, k=k)
        winner = np.argmax(self.all_fits[competitors]) # This indexation might fail
        pool.pop(winner) # remove winner from pool
        winners.append(winner)

    couples = list(zip(winners[::2],winners[1::2]))
    self.mates = couples # ?????

def ranked(self, qnt_pairs):
    idxs  = range(self.population)
    aux = reversed(idxs)
    probs = list(map(sum(aux).__rtruediv__, aux))

    fitness = lambda x: self.all_fits[x]
    ranks = sorted(idxs, key=fitness)
    
    winners = []
    for i in range(2*qnt_pairs):
        winner = choice(ranks, p=probs)
        ranks.pop(winner)
        probs.pop(winner)
        winners.append(winner)

    couples = list(zip(winners[::2],winners[1::2]))
    self.mates = couples # ?????
    

        
class Test:
    def __init__(self):
        self.population = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]]
        self.population += [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]]
        self.population = list(map(np.asarray, self.population))
        self.all_fits = [3,7,2,5,6,7,9,0,2,-1]
        self.mates = None

test = Test()
tournament(test, 4, 2)
print(test.mates)