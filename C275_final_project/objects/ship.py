import pygame, math
import objects
from objects.baseObject import BaseObject

class Ship(BaseObject):
    """
    Ship. Controlled with arrow keys and spacebar. Flies through space, without
    colliding with asteroids (design decision), shooting missiles to destroy
    asteroids and aliens.
    """    
    sprite = pygame.image.load('assets/ship.gif')
    shipGroup = pygame.sprite.Group()
    def __init__(self, **keywords):
        #loads the base class
        super().__init__(**keywords)
        self._layer = 2
        self.health = 5
        self.position = (200,100)
        # Needs two for rotations
        self.src_image = Ship.sprite
        self.image = self.src_image.convert()
        self.rect = self.image.get_rect()
        # Physics and movement attributes
        self.mass = 10
        self.max_speed = 12
        self.turn_speed = 7
        self.acceleration = 1
        self.damage = 0.5

        # User input tracking variables
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self):
        # Updates speed
        self.speed += (self.k_up - self.k_down)
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < 0:
            self.speed = 0
        # Updates direction
        self.direction += (self.k_left - self.k_right)
        # Update position
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed*math.cos(rad)
        y += -self.speed*math.sin(rad)
        self.position = (x, y)        
        # Rotate image
        self.image = pygame.transform.rotate(self.src_image, self.direction-90)
        
        # Update rect
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def fire_missile(self):
        objects.missile.Missile.missileGroup.add(
            objects.object_types["missile"]\
                (position = self.position, 
                 direction = self.direction))

objects.object_types["ship"] = Ship
