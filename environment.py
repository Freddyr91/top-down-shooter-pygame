from settings import *

class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos * TILESIZE

class Floor(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = FLOOR_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(game.floor_imgs)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos * TILESIZE