import pygame, math
import objects
from objects.baseObject import BaseObject

class Beam(BaseObject):
    """
    the visual effect for an alien jumping between asteroids (colored line)
    """       
    beamGroup = pygame.sprite.Group()
    def __init__(self, obj1, obj2, color, surface, health = 5,**keywords):
        #loads the base class
        super().__init__(**keywords)
        self.call_time = None        
        self.surface = surface
        self.color = color
        #health determines how long the effect lasts
        self.health = health
        self.obj1 = obj1
        self.obj2 = obj2

    def update(self):
        # Update position
        self.hurt(1)
        self.rect = \
            pygame.draw.line(
            self.surface, self.color, 
            self.obj1.position, self.obj2.position)

objects.object_types["beam"] = Beam
