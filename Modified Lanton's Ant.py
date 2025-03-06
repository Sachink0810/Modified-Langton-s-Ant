import pygame as pg
from collections import deque
from random import randrange,random,randint


class Ant:

    def __init__(self,main,pos,color):
        self.main = main
        self.color = color
        self.x,self.y = pos
        self.increment = deque([(1,0),(0,1),(-1,0),(0,-1)]) # Directional movements
        self.increment.rotate(randint(1,4)) # Ants to have a random direction to move on spawn
        self.pheromone = {} #initialising pheromones as dictionary using coordinates as keys and strength as values

    def move(self,pheromone2):
        value = self.main.grid[self.y][self.x] # value for changes in colour
        self.main.grid[self.y][self.x] = not value

        Size = self.main.Cell_size
        rect = self.x * Size, self.y * Size, Size - 1 , Size - 1

        if value:
            pg.draw.rect(self.main.screen,'white',rect)
        else:
            pg.draw.rect(self.main.screen,self.color,rect)

        # function to handle all pheromone interactions
        self.pheromone_inter(pheromone2,value)

        # addition of pheromone on new cell and removal of old if any
        if (self.x,self.y) in list(pheromone2.keys()):
            del pheromone2[(self.x,self.y)]
        self.pheromone[(self.x,self.y)] = 5

        # Moving the ants according to pheromone interaction
        dx,dy = self.increment[0]
        self.x = (self.x + dx) % self.main.Cols # Taking mod so that ant doesnt go outside screen
        self.y = (self.y + dy) % self.main.Rows

        # pheromones decay on cells 
        for keys in list(self.pheromone.keys()):
            self.pheromone[keys] -= 1
            if self.pheromone[keys] == 0:
                del self.pheromone[keys]

    #pheromone interaction function
    
    def pheromone_inter(self,pheromone2,value):
        if (self.x,self.y) in self.pheromone:
            self.prob = (0.8 / 5) * self.pheromone[(self.x,self.y)] # probablity of moving straight interacting with own pheromone

        elif (self.x,self.y) in pheromone2:
            self.prob = (0.2 / 5) * pheromone2[(self.x,self.y)] # probability of moving straight interacting with other pheromone

        else:
            self.prob = 0 # when no pheromone, it does not move straight forward without turning

        if random() >= self.prob: # rotating when needed
            self.increment.rotate(1) if value else self.increment.rotate(-1)
        
class Main:

    def __init__(self, Width = 1280, Height = 720,  Cell_size = 6):
        pg.init()
        self.screen = pg.display.set_mode((Width,Height))
        self.clock = pg.time.Clock()
        self.screen.fill('white')

        self.Cell_size = Cell_size 
        self.Rows, self.Cols = Height//Cell_size, Width//Cell_size
        self.grid = [[0 for col in range(self.Cols)] for row in range(self.Rows)]
        
        # Making grid
        for x in range(0,Width,Cell_size):
            pg.draw.line(self.screen,'grey',(x,0),(x,Height))
        for y in range(0,Height,Cell_size):
            pg.draw.line(self.screen,'grey',(0,y),(Width,y))
        
        # Spawning ants at random location
        self.ants = [Ant(self, [randrange(self.Cols),randrange(self.Rows)], 'black') for i in range(2)]

    def run(self):
        while True:
            # Calling ant's move function with others pheromone as parameter
            [self.ants[i].move(self.ants[(i + 1) % len(self.ants)].pheromone) for i in range(len(self.ants))]


            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    main = Main()
    main.run()
