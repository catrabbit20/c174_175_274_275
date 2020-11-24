import pygame, math
import objects
from objects.baseObject import BaseObject

class Missile(BaseObject):
    """
    Missile. A projectile that travels in a straight line from the nose of 
    the ship, and deals damage to the first asteroid it collides with. Is
    destroyed after collision.
    """       
    sprite = pygame.image.load('assets/missile_sm.png')
    missileGroup = pygame.sprite.Group()
    def __init__(self, **keywords):
        #loads the base class
        super().__init__(**keywords)
        self.image = Missile.sprite.convert()
        self.rect = self.image.get_rect()
        self.speed = 20
        self.health = 1
        self.mass = 2
        #self.call_time = None
        self.damage = 1

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

objects.object_types["missile"] = Missile
