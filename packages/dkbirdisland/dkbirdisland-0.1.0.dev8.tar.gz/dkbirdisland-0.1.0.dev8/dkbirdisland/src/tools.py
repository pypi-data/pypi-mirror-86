import pygame
import os

SRC_PATH = os.path.dirname(os.path.abspath(__file__))

def load_img(name):
    path = os.path.join(SRC_PATH ,'../images', name)
    return pygame.image.load(path)

