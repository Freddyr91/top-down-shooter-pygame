from settings import *

class MuzzleFlash(pg.sprite.Sprite):
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