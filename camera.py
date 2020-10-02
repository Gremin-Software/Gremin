#!/usr/bin/python
# -*- coding: utf-8 -*-

import characters


class Camera:
    def __init__(self):
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.current_pos = [self.pos_x, self.pos_y]

    def update_camera_pos(self, player: characters.Player, display_size: tuple) -> None:
        x_dist = player.pos_x - self.current_pos[0] - display_size[0] // 2
        y_dist = player.pos_y - self.current_pos[1] - display_size[1] // 2

        self.current_pos[0] += x_dist // 15
        self.current_pos[1] += y_dist // 15
