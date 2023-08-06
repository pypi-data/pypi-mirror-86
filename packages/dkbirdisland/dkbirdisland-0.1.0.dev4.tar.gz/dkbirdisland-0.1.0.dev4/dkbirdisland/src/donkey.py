import pygame
from . import tools

class Donkey(pygame.sprite.Sprite):
    def __init__(self, MIN_HEIGHT, SPEED_JUMP, GRAVITY):
        pygame.sprite.Sprite.__init__(self)

        self.images_walk = [tools.load_img('animations/Andar (1).png').convert_alpha(),
                            tools.load_img('animations/Andar (2).png').convert_alpha(),
                            tools.load_img('animations/Andar (3).png').convert_alpha(),
                            tools.load_img('animations/Andar (4).png').convert_alpha(),
                            tools.load_img('animations/Andar (5).png').convert_alpha(),
                            tools.load_img('animations/Andar (6).png').convert_alpha()]

        self.images_jump = [tools.load_img('animations/Jump (1).png').convert_alpha(),
                            tools.load_img('animations/Jump (2).png').convert_alpha(),
                            tools.load_img('animations/Jump (3).png').convert_alpha(),
                            tools.load_img('animations/Jump (4).png').convert_alpha(),
                            tools.load_img('animations/Jump (5).png').convert_alpha()]

        self.speed = 50

        self.current_image = 0
        self.image = tools.load_img('original.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] = 20
        self.rect[1] = 228

    def update(self, GRAVITY, MIN_HEIGHT):
        self.current_image = (self.current_image + 1) % 6
        self.image = self.images_walk[self.current_image]

        self.speed += GRAVITY
        self.rect[1] += self.speed

        if self.rect[1] > MIN_HEIGHT:
            self.rect[1] = MIN_HEIGHT
            self.speed = 0

    def jump(self, SPEED_JUMP, MIN_HEIGHT):
        if self.rect[1] == MIN_HEIGHT:
            self.speed = -SPEED_JUMP
