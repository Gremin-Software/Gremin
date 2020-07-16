#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import characters

pygame.init()
pygame.display.set_caption('Gremin')
WINDOW_SIZE = (480, 480)
main_window = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()  # used for setting FPS
run = True

tiles = [pygame.Rect(0, 400, 400, 60), pygame.Rect(410, 300, 60, 100),
         pygame.Rect(100, 200, 200, 10)]  # only for collision testing, do wyjebania :)

player_image = pygame.image.load('sprites/player.png')  # piwko ;)
gremin = characters.Player(50, 0, 40, 40, player_image, tiles)

enemy_image = pygame.image.load('sprites/STROJ-PASTUSZEK-kostium-ludowy-GORAL-baca-122-128.png')
enemy = characters.Enemy(200, 0, 40, 40, enemy_image, tiles)

while run:  # main loop

    main_window.fill((0, 0, 0))  # fills the background with black every frame

    # event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gremin.moving_right = True
            if event.key == pygame.K_LEFT:
                gremin.moving_left = True
            if event.key == pygame.K_UP:
                gremin.jumping = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gremin.moving_right = False
            if event.key == pygame.K_LEFT:
                gremin.moving_left = False

    for tile in tiles:
        pygame.draw.rect(main_window, (0, 255, 0), tile)  # draws the tiles from tiles list every frame

    gremin.move()
    gremin.draw(main_window)

    enemy.move()
    enemy.draw(main_window)

    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
