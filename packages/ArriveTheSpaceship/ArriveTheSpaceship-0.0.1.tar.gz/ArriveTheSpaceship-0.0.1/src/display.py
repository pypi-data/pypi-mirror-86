import pygame as pg

def initial_screen():
    pg.init()

    white = (255, 255, 255)
    black = (0, 0, 0)

    width = 1280
    height = 720
    name = 'Arrive the Spaceship'

    x_pos = width / 2
    y_pos = height / 2
    velocity = 10
    size = 10

    background = pg.display.set_mode((width, height))
    pg.display.set_caption(name)

    loop = True
    while loop:
        pg.time.delay(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
        
        command = pg.key.get_pressed()
        if command[pg.K_UP]:
            y_pos -= velocity
        elif command[pg.K_DOWN]:
            y_pos += velocity
        elif command[pg.K_LEFT]:
            x_pos -= velocity
        elif command[pg.K_RIGHT]:
            x_pos += velocity
        background.fill(black)

        pg.draw.rect(background, white, [x_pos, y_pos, size, size])
        
        pg.display.update()
    pg.quit()