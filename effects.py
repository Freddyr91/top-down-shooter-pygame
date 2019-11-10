import settings as conf
import utils

class Bullet(conf.pg.sprite.Sprite):
    def __init__(self, game, pos, dir, type):
        self._layer = conf.PLAYER_LAYER
        self.type = type
        self.groups = game.all_sprites, game.bullets
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_imgs[type]
        self.image_copy = self.image.copy()
        self.rot = dir.angle_to(conf.vec(1,0))
        self.image = conf.pg.transform.rotate(self.image_copy, self.rot)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * conf.WEAPONS[type]['speed'] * conf.random.uniform(0.9, 1.1)
        self.spawn_time = conf.pg.time.get_ticks()
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if conf.pg.sprite.spritecollideany(self, self.game.walls):
            if (conf.WEAPONS[self.type]['solid']):
                self.kill()
        if conf.pg.time.get_ticks() - self.spawn_time > conf.WEAPONS[self.type]['lifetime']:
            self.kill()

class Splat(conf.pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = conf.SPLAT_LAYER
        self.groups = game.all_sprites
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        img = conf.random.choice(game.splat_imgs)
        self.image = img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        dir = conf.vec(conf.random.uniform(-1.0, 1.0), conf.random.uniform(-1.0, 1.0))
        self.rot = (dir.angle_to(conf.vec(1, 0)))
        self.image = conf.pg.transform.rotate(img, self.rot)

class Flash(conf.pg.sprite.Sprite):
    def __init__(self, game, pos, rot):
        self._layer = conf.EFFECT_LAYER
        self.groups = game.all_sprites
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = conf.random.randint(20, 50)
        self.image = conf.pg.transform.scale(conf.random.choice(game.flash_imgs), (size * 2, size))
        self.image = conf.pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = conf.pg.time.get_ticks()

    def update(self):
        if conf.pg.time.get_ticks() - self.spawn_time > conf.BULLET_FLASH_DUR:
            self.kill()
