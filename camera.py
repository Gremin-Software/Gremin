#!/usr/bin/python
# -*- coding: utf-8 -*-

import characters


class Camera:
    def __init__(self, length: int, width: int):
        self.x: int = 0
        self.y: int = 0
        self.length = length
        self.width = width

    @property
    def current_pos(self):
        return self.x, self.y

    def update_camera_pos(self, player: characters.Player) -> None:
        x_dist = player.pos_x - self.x - self.length // 2
        y_dist = player.pos_y - self.y - self.width // 2

        self.x += x_dist // 15
        self.y += y_dist // 15
