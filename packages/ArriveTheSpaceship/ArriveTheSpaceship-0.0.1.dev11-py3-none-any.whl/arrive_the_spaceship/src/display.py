import pygame as pg
from pygame.locals import *

def initial_screen():
    pg.init()

    white = (255, 255, 255)
    black = (0, 0, 0)

    width = 1280
    height = 720
    name = 'Arrive the Spaceship'
    background = pg.image.load('media/surfaces/moon.jpg')
    
    monkey_up = pg.image.load('media/monkey/alive.png')
    monkey_left = pg.transform.rotate(monkey_up, 90)
    monkey_right = pg.transform.rotate(monkey_up, -90)
    monkey_down = pg.transform.rotate(monkey_up, 180)
    monkey = monkey_up
    
    x_pos = width / 2
    y_pos = 620
    velocity = 50
    size = 10

    display = pg.display.set_mode((width, height))
    pg.display.set_caption(name)

    loop = True
    while loop:
        command = pg.key.get_pressed()
        pg.time.delay(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
            if command[pg.K_UP]:
                y_pos -= velocity
                monkey = monkey_up
            elif command[pg.K_DOWN]:
                y_pos += velocity
                monkey = monkey_down
            elif command[pg.K_LEFT]:
                x_pos -= velocity
                monkey = monkey_left
            elif command[pg.K_RIGHT]:
                x_pos += velocity
                monkey = monkey_right
        
        display.blit(background, (0, 0))
        display.blit(monkey, (x_pos, y_pos))
        
        pg.display.update()
    pg.quit()