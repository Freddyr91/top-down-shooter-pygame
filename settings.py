import sys
from pygame.locals import *
import numpy as np
import random
import random
from os import path
import pygame as pg
import ctypes

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

#map properties
MAPS = ['map1.txt', 'map2.txt']
WALL_TILE = '1'
PLAYER_TILE = 'P'
HEALTH_TILE = 'H'
MOB_TILE = 'M'
MG_TILE = 'X'
SW_TILE = 'S'
SG_TILE = 'G'

#game properties
PLAYER_LAYER = 5
MOB_LAYER = 5
EFFECT_LAYER = 4
WALL_LAYER = 3
SPLAT_LAYER = 2
BG_LAYER = 1

TITLE = 'Space Shooter Thing'
FONT = 'FreePixel.ttf'
DEFAULT_FONT_SIZE = 30
BACKGROUND_IMAGE = 'background.jpg'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_IMGS = ['spaceship_still.png', 'spaceship_moving.png']
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(15, 0)

NOISE_IMGS = ['noise.png']
MOB_SIZES = ['normal', 'normal', 'normal', 'normal', 'normal', 'normal',
             'big',
             'small', 'small', 'small']
MOB_SPEED = 250
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_AVOID_RADIUS = 50
MOB_DETECT_RADIUS = 400
MOB_ROT_VEC = [vec(0,0), vec(0,1), vec(1,0), vec(1,1)]
MOB_DAMAGE_DELAY = 0.5

WALL_IMG = 'tile_98.png'

#effects
BULLET_FLASH_IMGS = []
for i in range(0, 1):
    BULLET_FLASH_IMGS.append('effect_0' + str(i) + '.png')
BULLET_FLASH_DUR = 40
SPLAT_IMGS = []
for i in range(0, 3):
    SPLAT_IMGS.append('splat_0' + str(i) + '.png')

# items
ITEM_IMGS = {'health': 'health.png',
             'machinegun': 'machinegun_pickup.png',
             'shotgun': 'shotgun_pickup.png',
             'shockwave': 'shockwave_pickup.png'}
ITEM_HEALTH_AMOUNT = 20
ITEM_BOB_RANGE = 16
ITEM_BOB_SPEED = 0.4

BG_MUSIC = 'through_space.ogg'
ENEMY_SOUNDS = []
for i in range(0,4):
    ENEMY_SOUNDS.append('noise' + str(i) + '.wav')
PLAYER_HIT_SOUNDS = []
for i in range(0,4):
    PLAYER_HIT_SOUNDS.append('hit' + str(i) + '.wav')
WEAPON_SOUNDS = {}
WEAPON_SOUNDS['gun'] = ['shoot1.wav', 'shoot2.wav', 'shoot3.wav', 'shoot4.wav',
                        'shoot5.wav', 'shoot6.wav', 'shoot7.wav', 'shoot8.wav']
EFFECTS_SOUNDS = {'level_start': 'weird.wav',
                  'health_up': 'pickup.wav',
                  'machinegun': 'space.wav',
                  'shotgun': 'space.wav',
                  'shockwave': 'space.wav'}


# Gun settings
BULLET_IMGS = {'pistol': 'bullet.png',
               'shotgun': 'bullet.png',
               'machinegun': 'bullet.png',
               'shockwave': 'shockwave.png'} 

WEAPONS = {} # Weapons dictionary

WEAPONS['pistol'] = {'ammo': -1,
                     'speed': 500,
                     'lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 20,
                     'bullet_count': 1,
                     'solid': True}

WEAPONS['machinegun'] = {'ammo': 200,
                         'speed': 500,
                         'lifetime': 1000,
                         'rate': 50,
                         'kickback': 400,
                         'spread': 5,
                         'damage': 10,
                         'bullet_count': 1,
                         'solid': True}

WEAPONS['shotgun'] = {'ammo': 12,
                      'speed': 20,
                      'lifetime': 500,
                      'rate': 900,
                      'kickback': 600,
                      'spread': 100,
                      'damage': 2,
                      'bullet_count': 42,
                      'solid': True}

WEAPONS['shockwave'] = {'ammo': 4,
                        'speed': 300,
                        'lifetime': 1500,
                        'rate': 1500,
                        'kickback': 300,
                        'spread': 0,
                        'damage': 7,
                        'bullet_count': 1,
                        'solid': False}