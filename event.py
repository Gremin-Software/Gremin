#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

import characters


def handle_events(gremin: characters.Player, display: pygame.Surface, run: bool):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gremin.moving_right = True
                gremin.last_movement_right = True
            if event.key == pygame.K_LEFT:
                gremin.moving_left = True
                gremin.last_movement_right = False
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
    return run
