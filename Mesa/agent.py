from mesa import Agent

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        self.state = state
        self.stop = state 
        self.timeToChange = timeToChange
    
    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass

class Intersection(Agent):
    def __init__(self, unique_id, model, node):
        super().__init__(unique_id, model)
        self.node = node

    def step(self):
        pass

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, pos, model, _destination):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        self.state = False 
        self.destination = _destination
        self.currIntersection = "B"
        self.nextIntersection = "B"
        self.pos = pos
        print("starting point: " , self.pos)
        print("destination: " , self.destination)

        super().__init__(unique_id, model)

    def wrong_way(self, i):
        # print(i)
        contents = self.model.grid.get_cell_list_contents(self.pos)
        road_direction = ()
        for a in contents:
            if isinstance(a, Road):
                if(a.direction == "Left"):
                    road_direction = (self.pos[0]-1, self.pos[1])
                elif(a.direction == "Right"):
                    road_direction = (self.pos[0]+1, self.pos[1])
                elif(a.direction == "Up"):
                    road_direction = (self.pos[0], self.pos[1]+1)
                elif(a.direction == "Down"):
                    road_direction = (self.pos[0], self.pos[1]-1)
                if abs(road_direction[0] - i[0]) == 2 or abs(road_direction[1] - i[1]) == 2:
                    return True
        # creo que solo lo de abajo es necesario
        contents = self.model.grid.get_cell_list_contents(i)
        road_direction = ()
        for a in contents:
            if isinstance(a, Road):
                if(a.direction == "Left"):
                    road_direction = (i[0]-1, i[1])
                elif(a.direction == "Right"):
                    road_direction = (i[0]+1, i[1])
                elif(a.direction == "Up"):
                    road_direction = (i[0], i[1]+1)
                elif(a.direction == "Down"):
                    road_direction = (i[0], i[1]-1)
                # print("road dir:", road_direction)
                # print("self.pos:", self.pos)
                if road_direction == self.pos:
                    return True
        return False

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        content = self.model.grid.get_cell_list_contents(self.pos)
        direction = ""
        for i in content:
            if(isinstance(i, Road)):
                direction = i.direction
        
        coordenates = ()
        
        if(direction == "Left"):
            coordenates = (self.pos[0]-1, self.pos[1])
        elif(direction == "Right"):
            coordenates = (self.pos[0]+1, self.pos[1])
        elif(direction == "Up"):
            coordenates = (self.pos[0], self.pos[1]+1)
        elif(direction == "Down"):
            coordenates = (self.pos[0], self.pos[1]-1)

        content = self.model.grid.get_cell_list_contents(coordenates)
        for i in content:
            if(isinstance(i, Car)):
                return
            elif(isinstance(i,Traffic_Light)):
                if not i.state:
                    return

        self.model.grid.move_agent(self,coordenates)

    def moveGradient(self, destination):
        temp_possible_steps = [
            (self.pos[0]+1, self.pos[1]),
            (self.pos[0], self.pos[1]+1),
            (self.pos[0], self.pos[1]),
            (self.pos[0]-1, self.pos[1]),
            (self.pos[0], self.pos[1]-1)
        ]
        minimum = 10000
        direction = self.pos
        # print("temp_possible_steps:", temp_possible_steps)
        possible_steps = [
            (self.pos[0]+1, self.pos[1]),
            (self.pos[0], self.pos[1]+1),
            (self.pos[0], self.pos[1]),
            (self.pos[0]-1, self.pos[1]),
            (self.pos[0], self.pos[1]-1)
        ]
        for i in temp_possible_steps:
            # print("i =", i)
            if(i[0] < 0 or i[0] >= self.model.width or i[1] < 0 or i[1] >= self.model.height):
                # print("removing i:", i, "(out of bounds)")
                possible_steps.remove(i)   
            elif isinstance(self.model.grid.get_cell_list_contents(i)[0], Obstacle) or isinstance(self.model.grid.get_cell_list_contents(i)[0], Traffic_Light) or isinstance(self.model.grid.get_cell_list_contents(i)[0], Car):
                # print("removing i:", i, "(obstacle)")
                possible_steps.remove(i)  
            elif self.wrong_way(i):
                # print("removing i:", i, "(wrong way)")
                possible_steps.remove(i)
        # print("new possible_steps:", possible_steps)
        for step in range(0, len(possible_steps)):
            gradient = (abs(possible_steps[step][0] - destination[0]) + abs(possible_steps[step][1] - destination[1]))
            agent = self.model.grid.get_cell_list_contents(possible_steps[step])

            # there is not a Car in the cell
            if gradient < minimum: 
                for a in agent:
                    if isinstance(a, Traffic_Light) or isinstance(a, Obstacle) or isinstance(a, Car):
                        continue
                    else:
                        minimum = gradient 
                        direction = possible_steps[step]

        if direction == self.pos:
            self.move()
        else:
            agents = self.model.grid.get_cell_list_contents(direction)
            for a in agents:
                if(isinstance(a, Car)):
                    return
                if (isinstance(a, Destination)) and direction != self.destination:
                    self.move()
                    return
            self.model.grid.move_agent(self, direction)
        return
    
    def moveTrafficLight(self):
        possible_steps = [
            (self.pos[0]+1, self.pos[1]),
            (self.pos[0], self.pos[1]+1),
            (self.pos[0], self.pos[1]),
            (self.pos[0]-1, self.pos[1]),
            (self.pos[0], self.pos[1]-1)
        ]

        for i in possible_steps:
            if(i[0] < 0 or i[0] >= self.model.width or i[1] < 0 or i[1] >= self.model.height):
                possible_steps.remove(i)
        car = False
        intersection = False
        for step in range(0, len(possible_steps)):   
            agent = self.model.grid.get_cell_list_contents(possible_steps[step])
            for a in agent:
                if (isinstance(a, Car)):
                    car = True
                elif (isinstance(a,Intersection)):
                    intersection = True
            if not car and intersection:
                self.model.grid.move_agent(self,possible_steps[step])
                return
            car = False
            intersection = False
                    
        return

    def getIntersections(self):
        minimum = 10000
        intersection = ()
        for i in self.model.graph.intersection[self.nextIntersection]:
            gradient = abs(self.pos[0] - i[0]) + abs(self.pos[1] - i[1])
            if(gradient < minimum):
                minimum = gradient
                intersection = i
        return intersection

    
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """

        if(self.pos == self.destination):
            # print("borranding")
            self.model.killMePLS(self)
            return

        content = self.model.grid.get_cell_list_contents(self.pos)
        for i in content:
            if(isinstance(i, Intersection)):
                self.currIntersection = i.node # ola
                if(self.currIntersection == self.model.destinationIntersection[self.destination]):
                    self.nextIntersection = self.model.finalDestination[self.destination]
                    self.moveGradient(self.getIntersections())
                else:
                    self.nextIntersection = self.model.graph.next[self.currIntersection][self.model.destinationIntersection[self.destination]] 
                    self.moveGradient(self.getIntersections())
                break
            elif(isinstance(i,Road)):
                if(self.currIntersection == self.model.destinationIntersection[self.destination]):
                    self.moveGradient(self.destination)
                else:
                    self.move()
                break
            elif(isinstance(i,Traffic_Light)):
                self.moveTrafficLight()
                break
