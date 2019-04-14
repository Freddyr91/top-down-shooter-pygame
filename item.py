from settings import *
import pytweening as tween

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, itemType):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_imgs[itemType]
        self.image = pg.transform.scale(self.image, (round(TILESIZE/2), round(TILESIZE/2)))
        self.rect = self.image.get_rect()
        pos += vec(0.5, 0.5)
        self.pos = pos
        self.rect.center = pos * TILESIZE
        self.type = itemType
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        
    def update(self):
        # bobbing motion
        offset = ITEM_BOB_RANGE * (self.tween(self.step / ITEM_BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y * TILESIZE + offset * self.dir
        self.step += ITEM_BOB_SPEED * 60 / FPS
        if self.step > ITEM_BOB_RANGE:
            self.step = 0.0
            self.dir *= -1.0