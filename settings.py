import sys
from pygame.locals import *
import numpy as np
import random
from random import choice, randint, random, uniform
from os import path
import pygame as pg

vec = pg.math.Vector2

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
FPS = 144

MAPS = ['map1.txt', 'map2.txt']

#game properties
PLAYER_LAYER = 5
MOB_LAYER = 5
EFFECT_LAYER = 4
WALL_LAYER = 3
SPLAT_LAYER = 2
FLOOR_LAYER = 1

TITLE = 'Space Shooter Thing'
FONT = 'PIXEL-LI.TTF'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_IMGS = ['spaceship_still.png', 'spaceship_moving.png']
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(15, 0)

NOISE_IMGS = ['noise.png']
MOB_SIZES = ['normal', 'normal', 'normal', 'normal', 'normal', 'normal',
             'big',
             'small']
MOB_SPEED = 250
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50
MOB_DETECT_RADIUS = 400
MOB_ROT_VEC = [vec(0,0), vec(0,1), vec(1,0), vec(1,1)]

WALL_IMG = "tile_98.png"
FLOOR_IMGS = []
for i in range (0, 10):
    FLOOR_IMGS.append("tile_0" + str(i) + ".png")

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
WEAPON_SOUNDS = {}
WEAPON_SOUNDS['gun'] = ['shoot1.wav', 'shoot2.wav', 'shoot3.wav', 'shoot4.wav',
                        'shoot5.wav', 'shoot6.wav', 'shoot7.wav', 'shoot8.wav']
EFFECTS_SOUNDS = {'level_start': 'weird.wav',
                  'health_up': 'pickup.wav'}


# Gun settings
BULLET_IMGS = ["bullet.png"]
GUN_SPREAD = 3
SHOTGUN_SPREAD = 0
WEAPONS = {}
WEAPONS['pistol'] = {'speed': 500,
                     'lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 20,
                     'size': 'lg',
                     'count': 1}
WEAPONS['shotgun'] = {'speed': 400,
                      'lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 5,
                      'damage': 2,
                      'count': 15}