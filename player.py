from settings import *
from utils import *
import effects

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.image = pg.transform.scale(self.image,(48, 48))
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = pos * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.last_shot_shotgun = 0
        self.health = PLAYER_HEALTH
        self.weapon = "pistol"

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
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
        mouse_dir = vec(self.game.camera.mouseadjustment(pg.mouse.get_pos())) - vec(self.pos)
        self.rot = mouse_dir.angle_to(vec(1,0))
        ## TODO : add rotation if needed
        #self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                effects.Bullet(self.game, pos, dir.rotate(spread), self.weapon)
            self.game.soundManager.play_sound_effect(choice(self.game.weapon_sounds['gun']))
            effects.Flash(self.game, pos, self.rot)

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH