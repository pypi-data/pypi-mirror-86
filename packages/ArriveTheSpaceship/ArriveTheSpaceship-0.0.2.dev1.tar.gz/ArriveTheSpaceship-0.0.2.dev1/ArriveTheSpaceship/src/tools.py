import pygame
import os

HOME_DIR = os.path.split(os.path.abspath(__file__))[0]

def load_media(media):
    path = os.path.join(HOME_DIR ,'../media', media)
    return pygame.image.load(path)