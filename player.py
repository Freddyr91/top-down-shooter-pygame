from utils import *
import effects
import pygame as pg
import settings as conf
from random import uniform, choice

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = conf.PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_imgs[0]
        self.rect = self.image.get_rect()
        self.hit_rect = conf.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = conf.vec(0, 0)
        self.pos = pos * conf.TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.last_shot_shotgun = 0
        self.health = conf.PLAYER_HEALTH
        self.weapon = "pistol"
        self.points_current_level = 0

    def get_keys(self):
        self.vel = conf.vec(0, 0)
        keys = pg.key.get_pressed()
        speed = conf.PLAYER_SPEED
        if keys[pg.K_LSHIFT]:
            speed = speed * 1.4
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = speed
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if (pg.mouse.get_pressed()[0] == True):
            self.weapon = "pistol"
            self.shoot()
        if (pg.mouse.get_pressed()[2] == True):
            self.weapon = "shotgun"
            self.shoot()

    def update(self):
        self.get_keys()
        mouse_dir = conf.vec(self.game.camera.mouseadjustment(pg.mouse.get_pos())) - conf.vec(self.pos)
        self.rot = mouse_dir.angle_to(conf.vec(1,0))
        posBefore = self.pos
        self.pos += self.vel * self.game.dt
        if self.vel != conf.vec(0,0):
            self.image = pg.transform.rotate(self.game.player_imgs[1], self.rot)
        else:
            self.image = pg.transform.rotate(self.game.player_imgs[0], self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > conf.WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = conf.vec(1, 0).rotate(-self.rot)
            pos = self.pos + conf.BARREL_OFFSET.rotate(-self.rot)
            self.vel = conf.vec(-conf.WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(conf.WEAPONS[self.weapon]['count']):
                spread = uniform(-conf.WEAPONS[self.weapon]['spread'], conf.WEAPONS[self.weapon]['spread'])
                effects.Bullet(self.game, pos, dir.rotate(spread), self.weapon)
            self.game.soundManager.play_sound_effect(choice(self.game.weapon_sounds['gun']))
            effects.Flash(self.game, pos, self.rot)

    def add_health(self, amount):
        self.health += amount
        if self.health > conf.PLAYER_HEALTH:
            self.health = conf.PLAYER_HEALTH

    def add_points(self, pointsToAdd):
        self.points_current_level += pointsToAdd
