import settings as conf
import utils
import effects

class Mob(conf.pg.sprite.Sprite):
    def __init__(self, game, pos, forceNormal = False, rot = 0):
        self._layer = conf.MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        conf.pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.toughness = conf.random.uniform(0.9,1.2)
        self.mob_size = 'normal'
        if (not forceNormal):
            self.mob_size = conf.random.choice(conf.MOB_SIZES)
            if self.mob_size == 'big':
                self.toughness = conf.random.uniform(1.5,1.8)
            elif self.mob_size == 'small':
                self.toughness = conf.random.uniform(0.3,0.6)
        self.select_mob_img()
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = conf.MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = pos * conf.TILESIZE
        self.vel = conf.vec(0, 0)
        self.acc = conf.vec(0, 0)
        self.rect.center = pos * conf.TILESIZE
        self.rot = rot
        self.health = round(conf.MOB_HEALTH * self.toughness)
        self.speed = conf.MOB_SPEED / self.toughness
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < conf.MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()

    def select_mob_img(self):
        #TODO clean this
        image = conf.random.choice(self.game.noise_imgs)
        img_size = image.get_rect().size

        mob_size = round(conf.TILESIZE/2 * self.toughness)

        x = conf.random.randint(0, img_size[0] - mob_size)
        y = conf.random.randint(0, img_size[1] - mob_size)

        newimg = conf.pg.Surface((mob_size, mob_size)).convert_alpha()
        newimg.blit(image, (0, 0), (x,y, mob_size, mob_size))

        self.image = newimg


    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < conf.MOB_DETECT_RADIUS**2:
            if conf.random.random() < 0.001:
                self.game.soundManager.play_sound_effect(conf.random.choice(self.game.enemy_sounds))

            self.rot = (target_dist).angle_to(conf.vec(1, 0))
            ## TODO - Add rotation if needed
            self.image = conf.pg.transform.rotate(self.image_copy, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = conf.vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            utils.collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            utils.collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

        bullet_hits = conf.pg.sprite.spritecollide(self, self.game.bullets, False, utils.collide_hit_rect)
        for bullet in bullet_hits:
            self.health -= conf.WEAPONS[bullet.type]['damage']
            if (conf.WEAPONS[bullet.type]['solid']):
                self.vel = conf.vec(0,0)
                bullet.kill()

        if self.health <= 0:
            self.game.soundManager.play_sound_effect(conf.random.choice(self.game.enemy_hit_sounds))
            effects.Splat(self.game, self.pos)
            if self.mob_size == 'big':
                Mob(self.game, (self.pos-conf.vec(1,0))/conf.TILESIZE, True, self.rot)
                Mob(self.game, (self.pos-conf.vec(0,1))/conf.TILESIZE, True, self.rot)
                Mob(self.game, (self.pos+conf.vec(1,0))/conf.TILESIZE, True, self.rot)
                Mob(self.game, (self.pos+conf.vec(0,1))/conf.TILESIZE, True, self.rot)
            self.kill()
            self.game.player.add_points(100)
