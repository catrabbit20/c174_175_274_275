import pygame, math
import objects
from objects.baseObject import BaseObject

class Particle(BaseObject):
    """
    Visual effect, appears after something is destroyed (missile, asteroid,
    alien, space station, etc)
    """  
    particleGroup = pygame.sprite.Group()
    def __init__(self, radius, color, surface, health=5, **keywords):
        #loads the base class
        super().__init__(**keywords)
        self.call_time = None        
        self.damage = 2
        self.surface = surface
        self.color = color
        self.radius = radius
        self.health = health
        
    def update(self):
        # Update position
        self.hurt(1)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed*math.cos(rad)
        y += -self.speed*math.sin(rad)
        self.position = (int(x), int(y))
        
        self.rect = \
        pygame.draw.circle(self.surface,self.color, self.position, self.radius)

objects.object_types["particle"] = Particle
