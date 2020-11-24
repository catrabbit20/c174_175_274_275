import pygame
import objects
from objects.baseObject import BaseObject

class Score(BaseObject):
    """
    Score. Keeps track of the time lasted, space station health, and aliens 
    killed
    """
    scoreGroup = pygame.sprite.Group()
    def __init__(self, spaceStation, time, **keywords):
        #loads the base class
        super().__init__(**keywords)
        pygame.init()

        self.score = 0
        self.font = pygame.font.Font(None, 35)
        self.color = (152, 132, 112)
        self.time = time
        self.spaceStation = spaceStation
        self.right = self.position[0]

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def increaseScore(self, amount):
        self.score +=  amount
  
    def update(self, current_time):
        elapsed = current_time - self.time

        self.image = self.font.render(
            "Space Station Healh: {:0>2d}   Time: {:0>2d}   Score: {:0>2d}"\
                .format(int(self.spaceStation.health),int(elapsed),int(self.score)), 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.right = self.right

objects.object_types["score"] = Score
