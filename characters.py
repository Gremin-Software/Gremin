#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Classes related to characters"""

import pygame


class Character:
    gravity = 1
    char_rect_dict = {}

    def __init__(self, pos_x, pos_y, width, height, health, tiles, death_sound, movement_vel=5, jump_vel=20,
                 terminal_vel=15):
        self.health = health
        self.pos_x = pos_x  # player position
        self.pos_y = pos_y  #
        self.width = width
        self.height = height
        self.moving_right = False
        self.moving_left = False
        self.last_movement = 'right'  # direction of last horizontal movement
        self.movement_vel = movement_vel
        self.jumping = False
        self.can_jump = False
        self.jump_vel = jump_vel
        self.terminal_vel = terminal_vel
        self.fall_vel = 0
        self.player_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)  # used in collision_test()
        self.tiles = tiles  # tiles used in collision_test()
        Character.char_rect_dict[self] = self.player_rect  # adds to the dict (class instance ref: self.player_rect)
        self.death_sound = death_sound

    def movement_collision_test(self, tiles) -> list:
        """Returns a list of rectangles(tiles) the character is colliding with"""

        collisions = []
        self.player_rect.x = self.pos_x
        self.player_rect.y = self.pos_y
        for tile in tiles:
            if self.player_rect.colliderect(tile):  # checks whether the player collides with a rectangle(tile)
                collisions.append(tile)
        return collisions

    def move(self):
        """Character movement, jumping and collisions. Podjebany pomysl z neta."""

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
        collisions = self.movement_collision_test(self.tiles)
        for tile in collisions:
            if movement[0] > 0:
                self.pos_x = tile.left - self.width
                collision_types['right'] = True
            elif movement[0] < 0:
                self.pos_x = tile.right
                collision_types['left'] = True
        self.pos_y += movement[1]
        collisions = self.movement_collision_test(self.tiles)
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

    def check_if_dead(self):
        """
        Checks if a Character has died
        please see reference:
        https://stackoverflow.com/questions/47034604/how-do-i-delete-displayed-objects-in-python-with-pygame
        answer #2
        """
        if self.health <= 0 or self.pos_y >= 1500:
            Character.char_rect_dict.pop(self)
            pygame.mixer.music.load(self.death_sound)
            pygame.mixer.music.play()
            return True
        else:
            return False


class Player(Character):
    def __init__(self, pos_x, pos_y, width, height, health, image, tiles, death_sound, movement_vel=3, jump_vel=15, terminal_vel=5):
        super().__init__(pos_x, pos_y, width, height, health, tiles, death_sound, movement_vel, jump_vel, terminal_vel)
        self.image = image
        self.attack_damage = 20
        self.attack_range_x = 200
        self.attack_range_y = 20
        self.attack_rect = pygame.Rect(0, 0, self.attack_range_x, self.attack_range_y)
        self.is_attacking = False  # mozliwe ze bedzie mozna przeniesc do class Character
        self.respawn_x = pos_x
        self.respawn_y = pos_y
        self.respawn_hp = health

    def draw(self, display, camera_pos):  # draws the player to the screen, no animations for now, just a harnas
        # window.blit(self.image, (self.pos_x, self.pos_y))  # STARE
        if self.last_movement == 'right':
            display.blit(self.image, (self.pos_x - camera_pos[0], self.pos_y - camera_pos[1]))
        else:
            display.blit(pygame.transform.flip(self.image, True, False), (self.pos_x - camera_pos[0], self.pos_y - camera_pos[1]))

    def attack_collision_test(self, char_dict):
        """Returns a list of character instances the character attack hit box is colliding with"""

        collisions = []

        if self.last_movement == 'right':
            self.attack_rect.x = self.pos_x
        else:
            self.attack_rect.x = self.pos_x - self.attack_range_x + self.width
        self.attack_rect.y = self.pos_y + (self.height - self.attack_range_y) // 2

        for char in char_dict:
            rect = char_dict[char]
            if self.attack_rect.colliderect(rect):
                collisions.append(char)
        collisions.remove(self)
        print(collisions)  # TODO: WYJEBAC
        return collisions

    def attack(self):
        """Calls damage() function of damaged characters"""

        if self.is_attacking:
            collisions = self.attack_collision_test(Character.char_rect_dict)
            for char in collisions:
                char.damage(self.attack_damage)
            self.is_attacking = False

    def damage(self, damage):
        """Reduces the health by given damage"""

        self.health -= damage

    def draw_attack_hitbox(self, display):  # wyswietla hitboxa ataku  # PO ZAIMPLEMENTOWANIU KAMERY NIE DZIALA
        """TESTING FUNCTION"""

        test_rect = pygame.Rect(0, 0, self.attack_range_x, self.attack_range_y)
        if self.last_movement == 'right':
            test_rect.x = display.get_width() // 2
        else:
            test_rect.x = display.get_width() // 2 - self.attack_range_x + self.width
        test_rect.y = display.get_height() // 2 + (self.height - self.attack_range_y) // 2
        pygame.draw.rect(display, (255, 0, 0), test_rect)

    def respawn(self):
        """Gremin respawns on a paleta in the middle of the forest"""
        Character.char_rect_dict[self] = self.player_rect
        self.health = self.respawn_hp
        self.pos_x = self.respawn_x
        self.pos_y = self.respawn_y


class Enemy(Character):
    def __init__(self, pos_x, pos_y, width, height, health, image, tiles, death_sound, movement_vel=5, jump_vel=20, terminal_vel=15):
        super().__init__(pos_x, pos_y, width, height, health, tiles, death_sound, movement_vel, jump_vel, terminal_vel)
        self.image = image

    def draw(self, display, camera_pos):  # draws the player to the screen, no animations for now, just a goral
        display.blit(self.image, (self.pos_x - camera_pos[0], self.pos_y - camera_pos[1]))

    def damage(self, damage):
        self.health -= damage
        print(self, "health: ", self.health)  # TODO: WYJEBAC


class Paleta(Enemy):
    """Gremin respawn point. Inherits from class Enemy as for now - will be changed in the future"""
    def __init__(self, pos_x, pos_y, width, height, health, image, tiles, death_sound, movement_vel=0, jump_vel=20,
                 terminal_vel=15):
        super().__init__(pos_x, pos_y, width, height, health, image, tiles, death_sound, movement_vel, jump_vel,
                         terminal_vel)

    def set_respawn_place(self, gremin:Player):
        """Sets paleta as Gremin's respawn point when Gremin touches it"""
        if gremin.player_rect.colliderect(self.player_rect):
            gremin.respawn_x =  int(self.pos_x - self.width / 2)
            gremin.respawn_y = int(self.pos_y - 2 * self.height)

    def movement_collision_test(self, tiles) -> list:
        """Returns a list of rectangles(tiles) the character is colliding with"""

        collisions = []
        self.player_rect.x = self.pos_x
        self.player_rect.y = self.pos_y
        for tile in tiles:
            if self.player_rect.colliderect(tile) and tile != self.player_rect:  # prevents from colliding with itself
                collisions.append(tile)
        return collisions
