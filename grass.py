from settings import *

class Grass(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = FLOOR_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(game.grass_imgs)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos * TILESIZE