#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import characters


def get_camera_pos(player: characters.Player, current_pos: list, display_size: tuple) -> list:
    """Updates current camera position.
    TODO: napisac to jak czlowiek / zmienic sposob dzialania / wyjebac w pizdu
    TODO: szybkosc kamery zalezna od szybkosci gracza, ilosci pikseli na ekranie, a nie odgornie ustalonych liczb
    TODO: jesli nie uda sie skrocic to chyba dobrze by to bylo wrzucic do osobnego modulu
    """

    center_x = player.pos_x - display_size[0] // 2
    center_y = gremin.pos_y - display_size[1] // 2

    if current_pos[0] < center_x - 500:
        current_pos[0] += 100
    elif current_pos[0] < center_x - 200:
        current_pos[0] += 50
    elif current_pos[0] < center_x - 20:
        current_pos[0] += 3
    elif current_pos[0] < center_x:
        current_pos[0] += 1

    if current_pos[0] > center_x + 500:
        current_pos[0] -= 100
    elif current_pos[0] > center_x + 200:
        current_pos[0] -= 50
    elif current_pos[0] > center_x + 20:
        current_pos[0] -= 3
    elif current_pos[0] > center_x:
        current_pos[0] -= 1

    if current_pos[1] < center_y - 500:
        current_pos[1] += 100
    elif current_pos[1] < center_y - 200:
        current_pos[1] += 50
    elif current_pos[1] < center_y - 100:
        current_pos[1] += 5
    elif current_pos[1] < center_y:
        current_pos[1] += 2

    if current_pos[1] > center_y + 500:
        current_pos[1] -= 100
    elif current_pos[1] > center_y + 200:
        current_pos[1] -= 50
    elif current_pos[1] > center_y + 120:
        current_pos[1] -= 3
    elif current_pos[1] > center_y:
        current_pos[1] -= 1

    return current_pos


def load_map(path):
    """Loads a map from .txt"""
    with open(path + '.txt') as f:
        data = f.read()
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
DISPLAY_SIZE = (700, 400)
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

yoda = "sounds/yoda.mp3"  # sample death sound

player_image = pygame.image.load('sprites/player.png').convert()  # gremin
player_image.set_colorkey((255, 255, 255))
gremin = characters.Player(pos_x=50, pos_y=0, width=16, height=40, health=100, image=player_image, tiles=tiles,
                           death_sound=yoda)

camera_pos = [0, 0]  # initial camera position

enemy_image = pygame.image.load('sprites/STROJ-PASTUSZEK-kostium-ludowy-GORAL-baca-122-128.png').convert()
enemy_image.set_colorkey((255, 255, 255))
enemy = characters.Enemy(pos_x=200, pos_y=0, width=40, height=40, health=100, image=enemy_image, tiles=tiles,
                         death_sound=yoda)

paleta_image = pygame.image.load('sprites/paleta.png').convert()
paleta_image.set_colorkey((255, 255, 255))

paleta_1 = characters.Paleta(pos_x=300, width=40, height=12, image=paleta_image, tiles=tiles)
tiles.append(paleta_1.entity_rect)
paleta_2 = characters.Paleta(pos_x=500, pos_y=0, width=40, height=12, image=paleta_image, tiles=tiles)

entities = [enemy, gremin, paleta_1, paleta_2]  # list of entities so i can check stuff about them| used a list just
# to keep it extendable
characters = [enemy, gremin]  # added because some functions are exclusive for characters

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
                gremin.draw_attack_hitbox(display)  # TODO: WYJEBAC
            if event.key == pygame.K_r:  # TODO: WYJEBAC, przenosi gremina na mape
                gremin.pos_x = 50
                gremin.pos_y = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gremin.moving_right = False
            if event.key == pygame.K_LEFT:
                gremin.moving_left = False

    if gremin in entities:
        """
        Iterates through entities list which contains every Character that is alive
        and checks if that Character performs any allowed action.
        Adding this didn't brake anything YET and seems to be a good way to manage the increasing
        number of implemented Characters(I'm looking forward for flaku and more górals)
        """
        for entity in entities:
            if entity in characters and entity.check_if_dead():
                entities.remove(entity)
            else:
                entity.move()
                entity.draw(display, camera_pos)
                if entity is gremin:
                    entity.attack()
                elif entity.image == paleta_image:  # maybe it's better to check if entity is a Paleta object?
                    """Checks if gremin changes his respawn point"""
                    entity.set_respawn_place(gremin)

    else:
        gremin.respawn()
        entities.append(gremin)
    draw_map(map01, TILE_SIZE, display, DISPLAY_SIZE, camera_pos, dirt_img, grass_img)
    # camera_pos = [gremin.pos_x - DISPLAY_SIZE[0] // 2, gremin.pos_y - DISPLAY_SIZE[1] // 2]  # STARY SPOSOB DZIALANIA
    # zostawiam na wypadek zmiany
    camera_pos = get_camera_pos(gremin, camera_pos, DISPLAY_SIZE)  # nowy sposob. w razie czego zakomentowac

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
