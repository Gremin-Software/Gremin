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


def draw_map(game_map, tile_size, window, image_1, image_2):  # FUNKCJA BEDZIE DO ZMIANY JESLI DODAMY WIECEJ
    for y, layer in enumerate(game_map):                      # TEKSTUR/ZMIENIMY SPOSOB TWORZENIA MAPY
        for x, tile in enumerate(layer):
            if tile == '1':
                window.blit(image_1, (x * tile_size, y * tile_size))
            elif tile == '2':
                window.blit(image_2, (x * tile_size, y * tile_size))


pygame.init()
pygame.display.set_caption('Gremin')
WINDOW_SIZE = (480, 480)
display = pygame.display.set_mode(WINDOW_SIZE)
TILE_SIZE = 16
clock = pygame.time.Clock()  # used for setting FPS
run = True


map01 = load_map('maps/map01')
grass_img = pygame.image.load('sprites/grass.png')
dirt_img = pygame.image.load("sprites/dirt.png")
tiles = get_tiles(map01, TILE_SIZE)  # list of all tiles(rects)

player_image = pygame.image.load('sprites/player.png')  # piwko ;)
gremin = characters.Player(pos_x=50, pos_y=0, width=40, height=40, health=100, image=player_image, tiles=tiles)

enemy_image = pygame.image.load('sprites/STROJ-PASTUSZEK-kostium-ludowy-GORAL-baca-122-128.png')
enemy = characters.Enemy(pos_x=200, pos_y=0, width=40, height=40, health=100, image=enemy_image, tiles=tiles)

while run:  # main loop

    display.fill((0, 0, 0))  # fills the background with black every frame

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

    # for tile in tiles:
    #     pygame.draw.rect(main_window, (0, 255, 0), tile)  # draws the tiles from tiles list every frame
    draw_map(map01, TILE_SIZE, display, dirt_img, grass_img)

    gremin.move()
    gremin.attack()
    gremin.draw_attack_hitbox(display)  # TODO: WYJEBAC
    gremin.draw(display)

    enemy.move()
    enemy.draw(display)

    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
