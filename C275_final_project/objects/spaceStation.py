import pygame
import objects
from objects.baseObject import BaseObject

class SpaceStation(BaseObject):
    """
    Space station. For the most part, does not interact with anything. However,
    if an alien is within range, it will jump on the space station, dealing
    damage to it. If space station health reaches zero, the game is lost.
    """
    
    sprite = pygame.image.load("assets/spaceStation.gif")
    spaceStationGroup = pygame.sprite.Group()

    def __init__(self, **keywords):
        #loads the base class
        super().__init__(**keywords)

        #set object specific things:
        self.health = 1000
        self.speed = 50
        self.direction = 180

        self.image = SpaceStation.sprite.convert()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.radius = self.rect.w

objects.object_types["spaceStation"] = SpaceStation
