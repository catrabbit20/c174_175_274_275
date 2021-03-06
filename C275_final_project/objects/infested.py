import pygame, math
import objects
from objects.baseObject import BaseObject

class Infested(BaseObject):
    """
    The big asteroid from which aliens spawn
    """

    sprite = pygame.image.load('assets/infested.gif')
    infestedGroup = pygame.sprite.Group()
    
    def __init__(self, **keywords):
        #loads the base class
        super().__init__(**keywords)

        #set object specific things:
        self.image = Infested.sprite.convert()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.mass = 300
        self.aliens = 0

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

objects.object_types["infested"] = Infested
