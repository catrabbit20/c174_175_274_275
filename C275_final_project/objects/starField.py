import pygame, math, random
import objects
from objects.baseObject import BaseObject

class StarField():
    """
    Starfield, moves above the background image of the game.
    
    Special class, required custom draw method for repeating image
    """
    starFieldGroup = pygame.sprite.Group()
    
    def __init__(self,speed, surface,**keywords):
        #set object specific things:
        self.sprite_repeat = 4
        self.image = \
            pygame.image.load('assets/starfield.png').convert_alpha(surface)
        self.rect = self.image.get_rect()
        self.left = 0
        self.speed = speed

    def update(self):
        # Update position
        self.left = (self.left+self.speed)%-self.rect.width
    
    def draw(self, surface):
        for i in range(self.sprite_repeat):
            surface.blit(self.image, (self.left+self.rect.w*i,0))
        

objects.object_types["starField"] = StarField
