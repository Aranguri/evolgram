import time
from heapq import heapify, heappop, heappush
import numpy as np
from numpy.random import choice, randint
import itertools

epsilon = 0.01
max_length = 99

class Env:
    def __init__(self, agents_amount):
        self.agents = [(0, []) for _ in range(agents_amount)]
        heapify(self.agents)

    def main(self):
        for i in itertools.count():
            self.get_fitness()
            self.diagnose(i)
            time.sleep(.1)
            half_population = int(len(self.agents) / 2)
            self.agents = self.agents[half_population:] # Remove first half of the agents
            all_fitness = np.array([agent[0] for agent in self.agents])
            weights = all_fitness / sum(all_fitness)
            old_agents = [agent for agent in self.agents] # Make a copy

            for _ in range(half_population):
                print (len(old_agents), len(weights))
                #Select parents
                index1, index2 = [choice(len(old_agents), p=weights) for _ in range(2)]
                code1, code2 = [old_agents[i][1] for i in [index1, index2]]
                #Crossover
                slice = randint(len(code1) + 1)
                child_code = code1[:slice] + code2[slice:]
                #Mutation
                child_code = self.mutate(child_code)

                heappush(self.agents, (0, child_code))

    def get_fitness(self):
        new_agents = []
        while len(self.agents):
            x, y, z = [randint(30) for _ in range(3)]
            correct_answer = x + y + z
            code = heappop(self.agents)[1]
            for line in code:
                locls = {'x': x, 'y': y, 'z': z}
                exec(line, {}, locls)
                x, y, z = [local for local in locls.values()]
            fitness = 1 / (abs(correct_answer - z) + epsilon) - len(code)
            heappush(new_agents, (fitness, code))

        self.agents = new_agents

    def mutate(self, code):
        mutation = randint(8) #We don't want to mutate all the time
        if mutation == 0 and len(code) != 0:   #Remove one line
            line = randint(len(code))
            del code[line]

        elif mutation == 1 and len(code) != 0: #Swap two lines
            line1, line2 = [randint(len(code)) for _ in range(2)]
            aux_line = code[line1]
            code[line1] = code[line2]
            code[line2] = aux_line

        elif mutation == 2 and len(code) < max_length: #Add one line
            var1, var2, var3 = [choice(['x', 'y', 'z']) for _ in range(3)]
            code.append('{} = {} + {}'.format(var1, var2, var3))

        return code

    def diagnose(self, i):
        avg_fitness = sum([agent[0] for agent in self.agents])
        best_fitness, best_code = self.agents[-1]

        print('Step {}'.format(i))
        print('Average fitness: {}'.format(avg_fitness))
        print('Best fitness: {}'.format(best_fitness))
        print('Best code')
        for line in best_code: print(line)
        '''
        for fitness, code in self.agents:
            for line in code:
                print(line)
            print('-' * 10)
        '''

class Agent:
    def __init__(self):
        self.fitness = 0
        self.program

env = Env(10)
env.main()
