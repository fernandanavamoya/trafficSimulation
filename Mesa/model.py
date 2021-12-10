from typing import Tuple
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json, secrets

class Graph(Model):
    def __init__(self, adj):
        self.intersection = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        self.adjacent = adj
        self.next = [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ]

        for i in range(11):
            for j in range(len(self.next[i])):
                if self.adjacent[i][j] != 1000:
                    self.next[i][j] = j
        
        # se rellena la matriz - Floyd Warshall Algorithm
        for k in range(len(self.adjacent)):
            for i in range(len(self.adjacent)):
                for j in range(len(self.adjacent)):
                    if(self.adjacent[i][j] > (self.adjacent[i][k] + self.adjacent[k][j])):
                        self.adjacent[i][j] = self.adjacent[i][k] + self.adjacent[k][j]
                        self.next[i][j] = self.next[i][k]

    
     

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, _maxIterations):
        adjacent = [
            [0,6,1000,6,1000,1000,1000,1000,1000,1000,1000],
            [1000,0,1000,1000,1000,15,1000,1000,1000,1000,1000],
            [15,1000,0,1000,1000,1000,1000,1000,1000,1000,1000],
            [1000,1000,6,0,1000,1000,1000,6,1000,1000,1000],
            [1000,6,1000,6,0,1000,1000,1000,1000,1000,1000],
            [1000,1000,1000,1000,6,0,1000,1000,1000,6,1000],
            [1000,1000,6,1000,1000,1000,0,6,1000,1000,1000],
            [1000,1000,1000,1000,1000,1000,1000,0,6,1000,6],
            [1000,1000,1000,1000,6,1000,1000,1000,0,6,1000],
            [1000,1000,1000,1000,1000,1000,1000,1000,1000,0,23],
            [1000,1000,1000,1000,1000,1000,15,1000,1000,1000,0]
        ]

        self.graph = Graph(adjacent)
        self.destinationIntersection = {
            (2,12) : 6,
            (4,23) : 2,
            (5,18) : 3,
            (7,5) : 7,
            (10,21) : 0,
            (14,7) : 7,
            (15,12) : 8,
            (19,2) : 9,
            (22,18) : 5,
            (23,5) : 9,
            (23,23) : 1,
        }

        self.finalDestination = {
            (2,12) : 2,
            (4,23) : 0,
            (5,18) : 2,
            (7,5) : 10,
            (10,21) : 3,
            (14,7) : 8,
            (15,12) : 4,
            (19,2) : 10,
            (22,18) : 4,
            (23,5) : 10,
            (23,23) : 5,
        }

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = RandomActivation(self)
            self.roads = []
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.roads.append((c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "A":
                        agent = Intersection(f"i{r*self.width+c}", self, 10)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.graph.intersection[10].append((c, self.height - r - 1))
                    elif col.isdigit():
                        agent = Intersection(f"i{r*self.width+c}", self, int(col))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.graph.intersection[int(col)].append((c, self.height - r - 1))
            
        self.num_agents = N
        foundCar = False

        counter = 0
        while counter < N:
            road = secrets.choice(self.roads)
            contents = self.grid.get_cell_list_contents(road)
            for i in contents:
                if isinstance(i, Car):
                    foundCar = True
            if(foundCar == False):
                new_car = Car(counter, road, self, secrets.choice(list(self.destinationIntersection.keys())))
                self.grid.place_agent(new_car, road)
                self.schedule.add(new_car)
                counter+=1
            foundCar = False
                
        self.maxIterations = _maxIterations
        self.iterations = 0
        self.running = True 
            
    def killMePLS(self, agent):
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)
        

    def step(self):
        print(Graph)
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        if not agent.state:
                            agent.stop = not agent.stop
                            if not agent.stop:
                                agent.state = not agent.state
                            
        if self.schedule.steps % 10 - 7 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        if agent.state:
                            agent.state = not agent.state
        self.iterations += 1
        if (self.iterations == self.maxIterations):
            self.running = False