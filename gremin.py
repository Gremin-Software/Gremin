#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

pygame.init()
pygame.display.set_caption('Gremin')
WINDOW_SIZE = (480, 480)
main_window = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()  # used for setting FPS
run = True


class Player:
    gravity = 1

    def __init__(self, pos_x, pos_y, width, height, image, movement_vel=5, jump_vel=20, terminal_vel=15):
        self.pos_x = pos_x  # player position
        self.pos_y = pos_y  #
        self.width = width
        self.height = height
        self.image = image  # just one image atm :d
        self.moving_right = False
        self.moving_left = False
        self.movement_vel = movement_vel
        self.jumping = False
        self.can_jump = False
        self.jump_vel = jump_vel
        self.terminal_vel = terminal_vel
        self.fall_vel = 0
        self.player_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)  # used in collision_test()

    def draw(self, window):  # draws the player to the screen, no animations for now, just a harnas
        window.blit(self.image, (self.pos_x, self.pos_y))

    def collision_test(self, tiles) -> list:
        """Returns a list of rectangles(tiles) the player is colliding with"""

        collisions = []
        self.player_rect.x = self.pos_x
        self.player_rect.y = self.pos_y
        for tile in tiles:
            if self.player_rect.colliderect(tile):  # checks whether the player collides with a rectangle(tile)
                collisions.append(tile)
        return collisions

    def move(self):
        """Player movement, jumping and collisions. Podjebany pomysl z neta."""

        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        movement = [0, 0]
        if self.moving_right:
            movement[0] += self.movement_vel
        if self.moving_left:
            movement[0] -= self.movement_vel

        movement[1] += self.fall_vel
        self.fall_vel += 1
        if self.fall_vel > self.terminal_vel:
            self.fall_vel = self.terminal_vel

        self.pos_x += movement[0]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if movement[0] > 0:
                self.pos_x = tile.left - self.width
                collision_types['right'] = True
            elif movement[0] < 0:
                self.pos_x = tile.right
                collision_types['left'] = True
        self.pos_y += movement[1]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if movement[1] > 0:
                self.pos_y = tile.top - self.height
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.pos_y = tile.bottom
                collision_types['top'] = True

        if collision_types['bottom'] or collision_types['top']:
            self.fall_vel = 0
        if collision_types['bottom']:
            self.can_jump = True
        if self.jumping and self.can_jump:
            self.fall_vel = -self.jump_vel
            self.can_jump = False
        self.jumping = False


tiles = [pygame.Rect(0, 400, 400, 60), pygame.Rect(410, 300, 60, 100),
         pygame.Rect(100, 200, 200, 10)]  # only for collision testing, do wyjebania :)

player_image = pygame.image.load('sprites/player.png')  # piwko ;)
gremin = Player(50, 0, 40, 40, player_image)

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

    pygame.display.update()
    clock.tick(60)  # sets the FPS to 60 :))

pygame.quit()
