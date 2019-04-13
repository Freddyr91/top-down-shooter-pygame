import sys
from pygame.locals import *
import numpy as np
import random
from random import choice, randint, random, uniform
from os import path
import pygame as pg

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_hit_rect(one, two):
    if hasattr(two, "hit_rect") and hasattr(two, "type"):
        print (one.hit_rect, two.hit_rect)
        return one.hit_rect.colliderect(two.hit_rect)
    return one.hit_rect.colliderect(two.rect)

#HUD
def draw_player_health(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = health/100.0 * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if health > PLAYER_HEALTH * 0.6:
        col = GREEN
    elif health > PLAYER_HEALTH * 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
GREEN2 = (10, 200, 80)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

size = WIDTH, HEIGHT = 1024, 768
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
FPS = 60

#game properties
PLAYER_LAYER = 4
MOB_LAYER = 4
EFFECT_LAYER = 3
WALL_LAYER = 2
FLOOR_LAYER = 1

TITLE = 'some game'
FONT = 'PIXEL-LI.TTF'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(15, 0)

NOISE_IMG = "noise.png"
MOB_SPEEDS = [150, 180, 170, 225, 125]
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50
MOB_DETECT_RADIUS = 400
MOB_ROT_VEC = [vec(0,0), vec(0,1), vec(1,0), vec(1,1)]

WALL_IMG = "tile_98.png"
BULLET_IMG = "bullet.png"
GRASS_IMG = []
for i in range (0, 10):
    GRASS_IMG.append("tile_0" + str(i) + ".png")

#effects
BULLET_FLASH_IMGS = []
for i in range(0, 1):
    BULLET_FLASH_IMGS.append("effect_0" + str(i) + ".png")
BULLET_FLASH_DUR = 40
SPLAT_IMGS = []
for i in range(0, 3):
    SPLAT_IMGS.append("splat_0" + str(i) + ".png")

# items
ITEM_IMGS = {'health': 'health.png'}
ITEM_HEALTH_AMOUNT = 20
ITEM_BOB_RANGE = 16
ITEM_BOB_SPEED = 0.4

BG_MUSIC = 'through_space.ogg'
ENEMY_SOUNDS = []
for i in range(0,4):
    ENEMY_SOUNDS.append("noise" + str(i) + ".wav")
PLAYER_HIT_SOUNDS = []
for i in range(0,4):
    PLAYER_HIT_SOUNDS.append("hit" + str(i) + ".wav")
WEAPON_SOUNDS_GUN = ['shoot.wav']
EFFECTS_SOUNDS = {'level_start': 'weird.wav',
                  'health_up': 'pickup.wav'}


# Gun settings
BULLET_IMG = "bullet.png"
GUN_SPREAD = 3
SHOTGUN_SPREAD = 0
WEAPONS = {}
WEAPONS['pistol'] = {'speed': 500,
                     'lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'size': 'lg',
                     'count': 1}
WEAPONS['shotgun'] = {'speed': 400,
                      'lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'count': 12}