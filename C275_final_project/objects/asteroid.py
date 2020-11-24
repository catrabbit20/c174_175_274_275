import pygame, math, random
import objects
from objects.baseObject import BaseObject

class Asteroid(BaseObject):
    """
    Asteroid. Spawns on the right edge of the screen, travels to the left. Can
    be destroyed with repeated missile hits or if it goes off screen. Can be
    jumped upon by aliens.
    """
    sprite = pygame.image.load('assets/asteroid.gif')
    asteroidGroup = pygame.sprite.Group()
    
    def __init__(self, alien = None, **keywords):
        #loads the base class
        super().__init__(**keywords)

        #set object specific things:
       
        self.health = 6
        self.image = Asteroid.sprite.convert()
        self.rect = self.image.get_rect()        
        self.rect.center = self.position
        self.capacity = 1
        self.mass = 100
        self.alien = alien

    def update(self):
        # Update position
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed*math.cos(rad)
        y += -self.speed*math.sin(rad)
        self.position = (x, y)

        # Update rect
        self.rect = self.image.get_rect()
        self.rect.center = self.position

objects.object_types["asteroid"] = Asteroid
