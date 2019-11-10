import settings as conf

class Wall(conf.pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = conf.WALL_LAYER
        self.groups = game.all_sprites, game.walls
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos * conf.TILESIZE

class Background(conf.pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = conf.BG_LAYER
        self.groups = game.all_sprites
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.background_image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
