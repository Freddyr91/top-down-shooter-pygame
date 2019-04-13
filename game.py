import pygame as pg
from settings import *
from map import *
from environment import *
from camera import *
from item import *
from player import *
from mob import *
from bullet import *

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
#        user32 = ctypes.windll.user32
#        screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#        print screenSize
#        size = (screenSize)
#        pg.display.set_mode((size) , pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        pg.mouse.set_cursor(*pg.cursors.broken_x)
        
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(self.asset_folder + "/" + font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname('__file__')
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.asset_folder = path.join(game_folder, 'assets')

        self.title_font = path.join(game_folder, FONT)
        self.dim_screen_img = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen_img.fill((0,0,0,120))
        
        self.map = Map(path.join(self.asset_folder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.noise_img = pg.image.load(path.join(img_folder, NOISE_IMG)).convert_alpha()
        self.grass_imgs = []
        for img in GRASS_IMG:
            self.grass_imgs.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.flash_imgs = []
        for img in BULLET_FLASH_IMGS:
            self.flash_imgs.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_imgs = {}
        for item in ITEM_IMGS:
            self.item_imgs[item] = pg.image.load(path.join(img_folder, ITEM_IMGS[item])).convert_alpha()
        self.splat_imgs = []
        for img in SPLAT_IMGS:
            foo = pg.image.load(path.join(img_folder, img)).convert_alpha()
            foo = pg.transform.scale(foo, (64, 64))
            self.splat_imgs.append(foo)
        # Sound
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effect_sounds = {}
        for type in EFFECTS_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
            s.set_volume(0.1)
            self.effect_sounds[type] = s
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(.1)
            self.weapon_sounds['gun'].append(s)
        self.enemy_sounds = []
        for snd in ENEMY_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(.2)
            self.enemy_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.enemy_hit_sounds = []
        for snd in ENEMY_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(.2)
            self.enemy_hit_sounds.append(s)
            

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                Grass(self, vec(col, row))
                if tile == '1':
                    Wall(self, vec(col, row))
                elif tile == 'P':
                    self.player = Player(self, vec(col, row))
                elif tile == 'H':
                    Item(self, vec(col, row), "health")
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'M':
                    Mob(self, vec(col, row))
                
        self.paused = False
                
        self.camera = Camera(self.map.width, self.map.height)
        self.effect_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused:
                self.update()                
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # player picks up health
        hits = pg.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effect_sounds['health_up'].play()
                self.player.add_health(ITEM_HEALTH_AMOUNT)
        # mob hits
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vec(0,0)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        #HUD
        draw_player_health(self.screen, 10, 10, self.player.health)
        self.draw_text("FPS " + "{:.2f}".format(self.clock.get_fps()), self.title_font, 24, WHITE, 120, 10, align = "nw")
        if self.paused:
            self.screen.blit(self.dim_screen_img, (0,0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH/2, HEIGHT/2, align = "center")
            self.draw_text("Press P to unpause game", self.title_font, 24, WHITE, WIDTH, 0, align = "ne")
        else:
            self.draw_text("Press P to pause game", self.title_font, 24, WHITE, WIDTH, 0, align = "ne")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass