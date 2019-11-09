import effects
import pygame as pg
import settings as conf
import utils
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
        self.main_weapon = "pistol"
        self.secondary_weapon = ""
        self.secondary_weapon_bullets = 0
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
            self.shoot(self.main_weapon)
        if (pg.mouse.get_pressed()[2] == True):
            if (self.secondary_weapon_bullets > 0):
                self.shoot(self.secondary_weapon)

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
        utils.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        utils.collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        # mob hits
        hits = pg.sprite.spritecollide(self, self.game.mobs, False, utils.collide_hit_rect)
        for hit in hits:
            if conf.random() < 0.7:
                self.game.soundManager.play_sound_effect(conf.choice(self.game.player_hit_sounds))
            self.health -= conf.MOB_DAMAGE
            hit.vel = conf.vec(0,0)
            if self.health <= 0:
                self.game.playing = False
        if hits:
            self.pos += conf.vec(conf.MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # player picks up health
        hits = pg.sprite.spritecollide(self, self.game.items, False, utils.collide_hit_rect)
        for hit in hits:
            if hit.type == "health" and self.health < conf.PLAYER_HEALTH:
                hit.kill()
                self.game.soundManager.play_sound_effect(self.game.effect_sounds['health_up'])
                self.add_health(conf.ITEM_HEALTH_AMOUNT)
            if (hit.type in conf.WEAPONS):
                hit.kill()
                self.game.soundManager.play_sound_effect(self.game.effect_sounds[hit.type])
                self.secondary_weapon = hit.type
                self.secondary_weapon_bullets = conf.WEAPONS[hit.type]['ammo']

    def shoot(self, weapon):
        now = pg.time.get_ticks()
        if now - self.last_shot > conf.WEAPONS[weapon]['rate']:
            self.last_shot = now
            dir = conf.vec(1, 0).rotate(-self.rot)
            pos = self.pos + conf.BARREL_OFFSET.rotate(-self.rot)
            self.vel = conf.vec(-conf.WEAPONS[weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(conf.WEAPONS[weapon]['count']):
                spread = uniform(-conf.WEAPONS[weapon]['spread'], conf.WEAPONS[weapon]['spread'])
                effects.Bullet(self.game, pos, dir.rotate(spread), weapon)
            if (weapon != self.main_weapon):
                self.secondary_weapon_bullets -= 1
            self.game.soundManager.play_sound_effect(choice(self.game.weapon_sounds['gun']))
            effects.Flash(self.game, pos, self.rot)

    def add_health(self, amount):
        self.health += amount
        if self.health > conf.PLAYER_HEALTH:
            self.health = conf.PLAYER_HEALTH

    def add_points(self, pointsToAdd):
        self.points_current_level += pointsToAdd
