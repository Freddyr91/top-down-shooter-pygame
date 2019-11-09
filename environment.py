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

class Floor(conf.pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = conf.FLOOR_LAYER
        self.groups = game.all_sprites
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = conf.choice(game.floor_imgs)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos * conf.TILESIZE
