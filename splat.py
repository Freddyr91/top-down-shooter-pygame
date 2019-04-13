from settings import *

class Splat(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = WALL_LAYER
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