import pytweening as tween
import settings as conf

class Item(conf.pg.sprite.Sprite):
    def __init__(self, game, pos, itemType):
        self._layer = conf.PLAYER_LAYER
        self.groups = game.all_sprites, game.items
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_imgs[itemType]
        self.image = conf.pg.transform.scale(self.image, (round(conf.TILESIZE/2), round(conf.TILESIZE/2)))
        self.rect = self.image.get_rect()
        pos += conf.vec(0.5, 0.5)
        self.pos = pos
        self.rect.center = pos * conf.TILESIZE
        self.type = itemType
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = conf.ITEM_BOB_RANGE * (self.tween(self.step / conf.ITEM_BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y * conf.TILESIZE + offset * self.dir
        self.step += conf.ITEM_BOB_SPEED * 60 / conf.FPS
        if self.step > conf.ITEM_BOB_RANGE:
            self.step = 0.0
            self.dir *= -1.0
