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
camera = camera.Camera(*DISPLAY_SIZE)

main_map = map.Map(map_file='maps/map01', tile_size=TILE_SIZE, camera=camera)

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
gremin = characters.Player(pos_x=50, pos_y=0, width=16, height=40, health=100, image=player_image, tiles=main_map.tiles,
                           death_sound=yoda)
enemy = characters.Enemy(pos_x=200, pos_y=0, width=40, height=40, health=100, image=enemy_image, tiles=main_map.tiles,
                         death_sound=yoda)
paleta_1 = characters.Paleta(pos_x=300, width=40, height=12, image=paleta_image, tiles=main_map.tiles, player=gremin)
paleta_2 = characters.Paleta(pos_x=500, pos_y=0, width=40, height=12, image=paleta_image, tiles=main_map.tiles, player=gremin)

entities = characters.Entity.entities_list  # list of entities

while run:  # main loop

    display.fill((51, 153, 255))  # fills the background with blue every frame

    # event handling
    run = event.handle_events(gremin, display, run)

    # camera position
    camera.update_camera_pos(gremin)
    camera_pos = camera.current_pos  # nowy sposob. w razie czego zakomentowac

    # updating and drawing entities
    for entity in entities:
        entity.update()
        entity.draw(display, camera_pos)

    main_map.draw(display)
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
