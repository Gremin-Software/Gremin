#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import characters


def load_map(path):
    """Loads a map from .txt"""

    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.splitlines()
    game_map = []
    for row in data:
        game_map.append(row)
    return game_map


def get_tiles(game_map, tile_size):  # DO ZMIANY JESLI ZMIENIMY SPOSOB TWORZENIA MAPY
    """Returns a list of rects"""

    tiles = []
    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile != '0':
                tiles.append(pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size))
    return tiles


def draw_map(game_map, tile_size, display, display_size, camera_pos, image_1, image_2):
    """Draws the map to the screen"""

    for y, layer in enumerate(game_map):                      # FUNKCJA BEDZIE DO ZMIANY JESLI DODAMY WIECEJ
        for x, tile in enumerate(layer):                      # TEKSTUR/ZMIENIMY SPOSOB TWORZENIA MAPY
            if tile == '1':
                display.blit(image_1, (x * tile_size - camera_pos[0], y * tile_size - camera_pos[1]))
            elif tile == '2':
                display.blit(image_2, (x * tile_size - camera_pos[0], y * tile_size - camera_pos[1]))


pygame.init()
pygame.display.set_caption('Gremin')
WINDOW_SIZE = (1440, 900)
DISPLAY_SIZE = (300, 200)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)
TILE_SIZE = 16
clock = pygame.time.Clock()  # used for setting FPS
run = True


map01 = load_map('maps/map01')
grass_img = pygame.image.load('sprites/grass.png')
dirt_img = pygame.image.load("sprites/dirt.png")
tiles = get_tiles(map01, TILE_SIZE)  # list of all tiles(rects)

player_image = pygame.image.load('sprites/player.png').convert()  # piwko ;)
player_image.set_colorkey((255, 255, 255))
gremin = characters.Player(pos_x=50, pos_y=0, width=16, height=40, health=100, image=player_image, tiles=tiles)

enemy_image = pygame.image.load('sprites/STROJ-PASTUSZEK-kostium-ludowy-GORAL-baca-122-128.png').convert()
enemy_image.set_colorkey((255, 255, 255))
enemy = characters.Enemy(pos_x=200, pos_y=0, width=40, height=40, health=100, image=enemy_image, tiles=tiles)

while run:  # main loop

    display.fill((51, 153, 255))  # fills the background with black every frame

    # event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gremin.moving_right = True
                gremin.last_movement = 'right'
            if event.key == pygame.K_LEFT:
                gremin.moving_left = True
                gremin.last_movement = 'left'
            if event.key == pygame.K_UP:
                gremin.jumping = True
            if event.key == pygame.K_SPACE:
                gremin.is_attacking = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gremin.moving_right = False
            if event.key == pygame.K_LEFT:
                gremin.moving_left = False

    camera_pos = [gremin.pos_x - DISPLAY_SIZE[0] // 2, gremin.pos_y - DISPLAY_SIZE[1] // 2]

    draw_map(map01, TILE_SIZE, display, DISPLAY_SIZE, camera_pos, dirt_img, grass_img)

    enemy.move()
    enemy.draw(display, camera_pos)

    gremin.move()
    gremin.attack()
    gremin.draw(display)
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
