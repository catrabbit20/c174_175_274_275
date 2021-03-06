import pygame, math
import objects
from objects.baseObject import BaseObject
from utilities import euclidD

class Alien(BaseObject):
    """
    Alien. Spawns from the big infested asteroid, jumps along path determined
    by max flow algorithm, reverts to greedy upon any path failure or if
    within range of space station. Deals damage to space station.
    """

    sprite = pygame.image.load('assets/alien.gif')
    alienGroup = pygame.sprite.Group()
    # Alien's teleport range
    radius = 300
    
    def __init__(self,asteroid = None, path=[],**keywords):
        #loads the base class
        super().__init__(**keywords)

        #set object specific things:
        self.health = 1
        self.image = Alien.sprite.convert()
        self.asteroid = asteroid
        self.rect = self.image.get_rect()
        self.rect.center = self.position = self.asteroid.position
        self.radius = Alien.radius
        self.damage = 8
        self.speed = 25
        self.path = path

    def update(self):
        # Update position
        if not self.asteroid is None:
            if not self.asteroid.alive():
                self.deactivate()
            else:
                self.position = self.asteroid.position
        # Update rect
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def deactivate(self):
        self.asteroid.alien = None
        self.kill()

    def path_hop(self, target):
        '''
        Primary Alien Movement
        Moves along the static path determined by max flow, 
        Fallback to greedy upon edge failure.
        '''
        curr = self.asteroid
        if curr == target: # we've made it to the target
            target.hurt(self.damage)
            self.deactivate()

        # Check if target's within reach
        elif pygame.sprite.collide_circle(target, self):
            curr.alien = None
            succ = target
            self.asteroid = succ
            self.path = None
            return (curr, succ)

        # Otherwise, continue along path
        elif len(self.path)>1: # 1 because last node will be spacestation
            succ = self.path.pop(0)
            if succ.alive():
                if succ.alien is None:
                    if pygame.sprite.collide_circle(succ, self):
                        curr.alien = None
                        succ.alien = self
                        self.asteroid = succ
                        return (curr,succ)
                    else: # No longer in range, go greedy and try to rejoin
                        return self.greedy_hop(target)
                else: # occupied, wait it out, should clear
                    pass
            else: # The asteroid is gone, go greedy move and try to rejoin
                return self.greedy_hop(target)
        else: # The target is next, or the path is ended, go greedy
            return self.greedy_hop(target)

    def greedy_hop(self, target):
        '''
        Fallback movement for the alien, picks in range asteroid closest
        to the mothership.        
        '''
        curr = self.asteroid
        if curr == target: # we've made it to the target
            target.hurt(self.damage)
            self.deactivate()

        # Check if target's within reach
        elif pygame.sprite.collide_circle(target, self):
            curr.alien = None
            succ = target
            self.asteroid = target
            return (curr,succ)

        # Check for better options
        else:
            distances = {}
            point1 = target.position

            for ast in objects.asteroid.Asteroid.asteroidGroup:
                # Check only if asteroid is free
                if ast.alien is None:
                    if pygame.sprite.collide_circle(self, ast):
                        point2 = ast.position
                        distances[ast] = euclidD(point1, point2)

            if not distances: # None in range
                pass

            else:
                succ = min(distances, key=distances.get)

                # Check if current is optimal
                if euclidD(point1, curr.position) < distances[succ]:
                    pass
                else:            
                    # we found an asteroid
                    # Clear parent asteroid's alien attribute
                    curr.alien = None

                    # Find and store child, set its alien attribute
                    succ.alien = self

                    # Set alien's asteroid attribute
                    self.asteroid = succ
                    return (curr,succ)

objects.object_types["alien"] = Alien
