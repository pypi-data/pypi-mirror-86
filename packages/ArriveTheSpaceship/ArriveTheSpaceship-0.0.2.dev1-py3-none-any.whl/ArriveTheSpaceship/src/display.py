from pygame import image
from .obstacle import Obstacle
from .monkey import Monkey
import pygame as pg
from . import tools

def initial_screen():
    pg.init()

    x_display = 1280
    y_display = 1000
    name = 'Arrive the Spaceship'
    pg.display.set_caption(name)
    background = tools.load_media(media="images/surfaces/moon.jpg")
    display = pg.display.set_mode((x_display, y_display))

    spike = Monkey()
    asteroid1 = Obstacle(image='red-asteroid.png', x_position='right', y_position=300)
    asteroid2 = Obstacle(image='red-asteroid.png', x_position='left', y_position=425)
    asteroid3 = Obstacle(image='red-asteroid.png', x_position='right', y_position=550)
    asteroid4 = Obstacle(image='red-asteroid.png', x_position='left', y_position=675)


    while True:
        
        pg.time.delay(15)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        
        spike.Load()
        asteroid1.Load(collision_reference=spike);
        asteroid2.Load(collision_reference=spike);
        asteroid3.Load(collision_reference=spike);
        asteroid4.Load(collision_reference=spike);
        
        display.blit(background, (0, 0))
        display.blit(spike.orientation, (spike.x_position, spike.y_position))
        display.blit(asteroid1.image, (asteroid1.x_position, asteroid1.y_position))
        display.blit(asteroid2.image, (asteroid2.x_position, asteroid2.y_position))
        display.blit(asteroid3.image, (asteroid3.x_position, asteroid3.y_position))
        display.blit(asteroid4.image, (asteroid4.x_position, asteroid4.y_position))
        
        pg.display.update()