import pygame
import sys
import random
from .donkey import Donkey
from .ground import Ground
from .obstacles import Obstacles
from .tools import load_img


def game():
    pygame.display.set_caption("Donkey Kong: Bird Island")

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 350
    GAME_SPEED = 20
    SPEED_JUMP = 50
    GRAVITY = 9
    GROUND_WIDTH = 2 * SCREEN_WIDTH
    GROUND_HEIGHT = 35
    MIN_HEIGHT = 228

    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    def get_random(sprite, width):
        return sprite.rect[0] <= width

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND = load_img("background.png")

    donkey_group = pygame.sprite.Group()
    donkey = Donkey(MIN_HEIGHT, SPEED_JUMP, GRAVITY)
    donkey_group.add(donkey)

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i, GROUND_WIDTH, GROUND_HEIGHT, GAME_SPEED, SCREEN_HEIGHT)
        ground_group.add(ground)

    obstacle_group = pygame.sprite.Group()
    obstacle = Obstacles(800, SCREEN_HEIGHT, GROUND_HEIGHT, GAME_SPEED)
    obstacle_group.add(obstacle)

    clock = pygame.time.Clock()

    # Principal
    verify = True
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    donkey.jump(SPEED_JUMP, MIN_HEIGHT)

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 50, GROUND_WIDTH, GROUND_HEIGHT, GAME_SPEED, SCREEN_HEIGHT)
            ground_group.add(new_ground)

        if len(obstacle_group.sprites()) > 0 and is_off_screen(obstacle_group.sprites()[0]):
            obstacle_group.remove(obstacle_group.sprites()[0])
            verify = True

        if get_random(obstacle_group.sprites()[0], 300) and verify:
            verify = False
            new_obstacle1 = Obstacles(random.randint(800, 1150), SCREEN_HEIGHT, GROUND_HEIGHT, GAME_SPEED)
            obstacle_group.add(new_obstacle1)


        donkey_group.update(GRAVITY, MIN_HEIGHT)
        obstacle_group.update(GAME_SPEED)
        ground_group.update(GAME_SPEED)

        donkey_group.draw(screen)
        obstacle_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        if pygame.sprite.groupcollide(donkey_group, obstacle_group, False, False, pygame.sprite.collide_mask):
            break
        clock.tick(20)

        
    
    pygame.quit()

