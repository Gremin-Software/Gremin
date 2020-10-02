#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame


def load(path):
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
                tiles.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
    return tiles


def draw(game_map, tile_size, display, camera_pos, image_1, image_2):
    """Draws the map to the screen"""

    for y, layer in enumerate(game_map):  # FUNKCJA BEDZIE DO ZMIANY JESLI DODAMY WIECEJ
        for x, tile in enumerate(layer):  # TEKSTUR/ZMIENIMY SPOSOB TWORZENIA MAPY
            if tile == '1':
                display.blit(image_1, (x * tile_size - camera_pos[0], y * tile_size - camera_pos[1]))
            elif tile == '2':
                display.blit(image_2, (x * tile_size - camera_pos[0], y * tile_size - camera_pos[1]))
