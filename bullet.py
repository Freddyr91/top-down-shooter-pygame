from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, type):
        self._layer = PLAYER_LAYER
        self.type = type
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * WEAPONS[type]['speed']
        self.spawn_time = pg.time.get_ticks()
        self.rot = dir.angle_to(vec(1,0))

    def update(self):
        self.image = pg.transform.rotate(self.game.bullet_img, self.rot)
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.type]['lifetime']:
            self.kill()