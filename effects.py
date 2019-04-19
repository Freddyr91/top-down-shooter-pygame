from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, type):
        self._layer = PLAYER_LAYER
        self.type = type
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(game.bullet_imgs)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * WEAPONS[type]['speed']
        self.spawn_time = pg.time.get_ticks()
        self.rot = dir.angle_to(vec(1,0))

    def update(self):
        self.image = pg.transform.rotate(choice(self.game.bullet_imgs), self.rot)
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.type]['lifetime']:
            self.kill()

class Splat(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = SPLAT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        img = choice(game.splat_imgs)
        self.image = img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        dir = vec(uniform(-1.0, 1.0), uniform(-1.0, 1.0))
        self.rot = (dir.angle_to(vec(1, 0)))
        self.image = pg.transform.rotate(img, self.rot)

class Flash(pg.sprite.Sprite):
    def __init__(self, game, pos, rot):
        self._layer = EFFECT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.flash_imgs), (size * 2, size))
        self.image = pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BULLET_FLASH_DUR:
            self.kill()
