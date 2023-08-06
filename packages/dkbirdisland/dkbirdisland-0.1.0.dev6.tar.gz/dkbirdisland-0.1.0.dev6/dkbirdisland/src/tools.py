import pygame
import os

SRC_PATH = os.path.split(os.path.abspath(__file__))[0]
IMAGES_PATH = os.path.join(SRC_PATH, '../images')

def load_img(name):
    path = os.path.join(IMAGES_PATH, name)
    return pygame.image.load(path)

