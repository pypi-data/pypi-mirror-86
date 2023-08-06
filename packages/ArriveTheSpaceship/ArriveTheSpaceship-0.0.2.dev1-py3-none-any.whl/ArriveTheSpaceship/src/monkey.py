import pygame as pg
from . import tools

class Monkey:
    
    def __init__(self):
        self.up = tools.load_media(media='images/monkey/alive.png')
        self.left = pg.transform.rotate(self.up, 90)
        self.right = pg.transform.rotate(self.up, -90)
        self.down = pg.transform.rotate(self.up, 180)
        self.orientation = self.up

        self.x_position = 640
        self.y_position = 917
        self.velocity = 5
    
    def Load(self):
        self.command = pg.key.get_pressed()

        if self.command[pg.K_UP]:
            self.orientation = self.up
            if self.y_position - self.velocity <= 0:
                self.y_position = 0
            else:
                self.y_position -= self.velocity
            
        if self.command[pg.K_DOWN]:
            self.orientation = self.down
            if self.y_position + self.velocity >= 917:
                self.y_position = 917
            else:
                self.y_position += self.velocity

        if self.command[pg.K_LEFT]:
            self.orientation = self.left
            if self.x_position - self.velocity <= 0:
                self.x_position = 0
            else:
                self.x_position -= self.velocity

        if self.command[pg.K_RIGHT]:
            self.orientation = self.right
            if self.x_position + self.velocity >= 1197:
                self.x_position = 1197
            else:
                self.x_position += self.velocity