from settings import *
from splat import *

class Mob(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.select_mob_img()
#        self.image = choice(game.mob_imgs).copy()
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = pos * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()
                    
    def select_mob_img(self):
        #TODO clean this
        image = self.game.noise_img
        img_size = image.get_rect().size
        
        mob_size = TILESIZE/2
        
        x = randint(0, img_size[0] - mob_size)
        y = randint(0, img_size[1] - mob_size)
        
        newimg = pg.Surface((mob_size, mob_size))
        newimg.blit(image, (0, 0), (x,y, mob_size, mob_size))        
        
        self.image = newimg
        

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < MOB_DETECT_RADIUS**2:
            if random() < 0.001:
                choice(self.game.enemy_sounds).play()
            
            self.rot = (target_dist).angle_to(vec(1, 0))
#            self.image = pg.transform.rotate(self.image_copy, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.enemy_hit_sounds).play()
            Splat(self.game, self.pos)
            self.kill()