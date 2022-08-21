#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import camera
from typing import Dict


def load(path):
    """Loads a map from .txt"""
    with open(path + ".txt") as f:
        return [row for row in f.read().splitlines()]


def get_tiles(game_map, tile_size):  # DO ZMIANY JESLI ZMIENIMY SPOSOB TWORZENIA MAPY
    """Returns a list of rects"""

    tiles = []
    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile != "0":
                tiles.append(
                    pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                )
    return tiles


def is_tile_visible(camera, x, y):
    return 0 <= x - camera.x <= camera.length and 0 <= y - camera.y <= camera.width


tile_mapping: Dict[str, pygame.Surface] = {
    "1": pygame.image.load("sprites/dirt.png"),
    "2": pygame.image.load("sprites/grass.png"),
}


class Map:
    def __init__(self, map_file: str, tile_size: int, camera: camera.Camera):
        self.game_map = load(map_file)
        self.tile_size = tile_size
        self.tiles = get_tiles(self.game_map, tile_size)
        self.camera = camera

    def draw(self, display):
        """Draws the map to the screen"""
        for y, layer in enumerate(self.game_map):
            for x, tile in enumerate(layer):
                if tile == "0" or not is_tile_visible(self.camera, x*self.tile_size, y*self.tile_size):
                    continue
                display.blit(
                    tile_mapping[tile],
                    (
                        x * self.tile_size - self.camera.x,
                        y * self.tile_size - self.camera.y,
                    ),
                )
