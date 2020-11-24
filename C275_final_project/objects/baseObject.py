import pygame, math
from pygame.sprite import Sprite

class BaseObject(Sprite):
   """
   the basic interstellar object from which all other interstellar objects
   extend.
   """
   def __init__(self, 
                position = (0,0),
                direction = 0,
                speed = 0,
                **keywords):
      Sprite.__init__(self)

      self.health = float("inf")
      self.max_health = self.health
      self.position = position
      self.image = None
      self.rect = None
      self.speed = speed
      self.direction = direction
         
   def deactivate(self):
      """
      Removes this unit from the active roster.
      """
      self.kill()

   def hurt(self, damage):
      """
      Causes damage to the unit, and destroys it when it's out of health.
      """
      self.health -= damage
        
      # Dead!
      if self.health <= 0:
         self.deactivate()
