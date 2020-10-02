#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import characters
import camera
import event
import map

pygame.init()
pygame.display.set_caption('Gremin')
WINDOW_SIZE = (1440, 900)
DISPLAY_SIZE = (700, 400)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)
TILE_SIZE = 16
clock = pygame.time.Clock()  # used for setting FPS
run = True
camera = camera.Camera()

map01 = map.load('maps/map01')
grass_img = pygame.image.load('sprites/grass.png')
dirt_img = pygame.image.load("sprites/dirt.png")
tiles = map.get_tiles(map01, TILE_SIZE)  # list of all tiles(rects)

# SOUNDS
yoda = "sounds/yoda.mp3"  # sample death sound

# PLAYER TEXTURE
player_image = pygame.image.load('sprites/player.png').convert()  # gremin
player_image.set_colorkey((255, 255, 255))

# ENEMY TEXTURE
enemy_image = pygame.image.load('sprites/STROJ-PASTUSZEK-kostium-ludowy-GORAL-baca-122-128.png').convert()
enemy_image.set_colorkey((255, 255, 255))

# PALETA TEXTURE
paleta_image = pygame.image.load('sprites/paleta.png').convert()
paleta_image.set_colorkey((255, 255, 255))

# ENTITIES
gremin = characters.Player(pos_x=50, pos_y=0, width=16, height=40, health=100, image=player_image, tiles=tiles,
                           death_sound=yoda)
enemy = characters.Enemy(pos_x=200, pos_y=0, width=40, height=40, health=100, image=enemy_image, tiles=tiles,
                         death_sound=yoda)
paleta_1 = characters.Paleta(pos_x=300, width=40, height=12, image=paleta_image, tiles=tiles, player=gremin)
paleta_2 = characters.Paleta(pos_x=500, pos_y=0, width=40, height=12, image=paleta_image, tiles=tiles, player=gremin)

entities = characters.Entity.entities_list  # list of entities

while run:  # main loop

    display.fill((51, 153, 255))  # fills the background with blue every frame

    # event handling
    run = event.handle_events(gremin, display, run)

    # camera position
    camera.update_camera_pos(gremin, DISPLAY_SIZE)
    camera_pos = camera.current_pos  # nowy sposob. w razie czego zakomentowac

    # updating and drawing entities
    for entity in entities:
        entity.update()
        entity.draw(display, camera_pos)

    map.draw(map01, TILE_SIZE, display, camera_pos, dirt_img, grass_img)
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
