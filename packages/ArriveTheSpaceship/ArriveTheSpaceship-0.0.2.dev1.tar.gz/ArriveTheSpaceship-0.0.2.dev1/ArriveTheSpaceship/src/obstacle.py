from ArriveTheSpaceship.src.monkey import Monkey
from . import tools
from random import randint
import pygame as pg
class Obstacle:
    def __init__(self, image, x_position, y_position):

        if x_position == 'right':
            self.x_spawn = randint(1400, 1900)
        elif x_position == 'left':
            self.x_spawn = randint(-500, -200)
        
        self.x_position = self.x_spawn 
        self.y_position = y_position
        self.image = tools.load_media(media='images/obstacles/' + image)
        self.velocity = randint(8, 12)
        self.num = int() # this will be used for tests

    def Load(self, collision_reference):
        
        if self.x_spawn >= 1400:
            self.x_position -= self.velocity
            if self.x_position < -125:
                self.x_position = randint(1400, 1900)
                self.velocity = randint(8, 12)
        
        elif self.x_spawn <= -200:
            self.x_position += self.velocity
            if self.x_position > 1280 + 25:
                self.x_position = randint(-700, -200)
                self.velocity = randint(8, 12)

        if self.x_position <= collision_reference.x_position + 50 <= self.x_position + 125: # in development
            if self.y_position <= collision_reference.y_position + 85 <= self.y_position + 125:
                # collision_reference.Change_sprite() -> this function still neds to be developed
                print('collision', self.num)
                self.num += 1