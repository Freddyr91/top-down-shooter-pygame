from os import path
import pygame as pg
import settings as conf
from environment import Background, Wall
from camera import Camera
from item import Item
from player import Player
from mob import Mob
from soundManager import SoundManager
from screenManager import ScreenManager
import utils

class Game:
    def __init__(self):
        self.soundManager = SoundManager()
        self.screenManager = ScreenManager(self)
        conf.pg.init()
        pg.display.set_caption(conf.TITLE)
        # Full-screen test stuff
        #user32 = conf.ctypes.windll.user32
        #screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        #print(screenSize)
        #size = (screenSize)
        #pg.display.set_mode((size) , pg.FULLSCREEN)
        #conf.WIDTH = screenSize[0]
        #conf.HEIGHT = screenSize[1]
        self.screen = conf.pg.display.set_mode((conf.WIDTH, conf.HEIGHT))
        #self.screen = conf.pg.display.set_mode((conf.WIDTH, conf.HEIGHT), pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        pg.mouse.set_cursor(*pg.cursors.broken_x)
        self.map_progress = 0
        self.points = 0
        self.player_health = 0
        self.seed = conf.random.randint(42, 69)

    def load_data(self):
        game_folder = path.dirname('__file__')
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        map_folder = path.join(game_folder, 'maps')
        self.asset_folder = path.join(game_folder, 'assets')

        self.title_font = path.join(game_folder, conf.FONT)
        self.background_image = utils.load_images_in_folder(conf.BACKGROUND_IMAGE, img_folder)
        self.dim_screen_img = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen_img.fill((0, 0, 0, 120))

        self.maps = utils.load_maps(map_folder)
        self.player_imgs = utils.load_images_in_folder(conf.PLAYER_IMGS, img_folder)
        for i in range(0, len(self.player_imgs)):
            self.player_imgs[i] = pg.transform.scale(self.player_imgs[i], (conf.TILESIZE, conf.TILESIZE))
        self.wall_img = utils.load_images_in_folder(conf.WALL_IMG, img_folder)
        self.bullet_imgs = utils.load_images_in_folder(conf.BULLET_IMGS, img_folder)
        self.noise_imgs = utils.load_images_in_folder(conf.NOISE_IMGS, img_folder)
        self.flash_imgs = utils.load_images_in_folder(conf.BULLET_FLASH_IMGS, img_folder)
        self.item_imgs = utils.load_images_in_folder(conf.ITEM_IMGS, img_folder)
        self.splat_imgs = utils.load_images_in_folder(conf.SPLAT_IMGS, img_folder)
        # Sound
        pg.mixer.music.load(path.join(music_folder, conf.BG_MUSIC))
        self.effect_sounds = utils.load_sounds_in_folder(conf.EFFECTS_SOUNDS, snd_folder)
        self.weapon_sounds = utils.load_sounds_in_folder(conf.WEAPON_SOUNDS, snd_folder)
        self.enemy_sounds = utils.load_sounds_in_folder(conf.ENEMY_SOUNDS, snd_folder)
        for s in self.enemy_sounds:
            s.set_volume(.2)
        self.player_hit_sounds = utils.load_sounds_in_folder(conf.PLAYER_HIT_SOUNDS, snd_folder)
        # TODO - Find other sound for this
        self.enemy_hit_sounds = utils.load_sounds_in_folder(conf.ENEMY_SOUNDS, snd_folder)
        for s in self.enemy_hit_sounds:
            s.set_volume(.2)

    def new(self):
        # initialize all variables and do all the setup for a new game
        conf.random.seed(self.seed)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for row, tiles in enumerate(self.maps[self.map_progress].data):
            for col, tile in enumerate(tiles):
                if tile == conf.WALL_TILE:
                    Wall(self, conf.vec(col, row))
                elif tile == conf.PLAYER_TILE:
                    self.player = Player(self, conf.vec(col, row))
                    if (self.player_health != 0):
                        self.player.health = self.player_health
                elif tile == conf.HEALTH_TILE:
                    Item(self, conf.vec(col, row), 'health')
                elif tile == conf.MG_TILE:
                    Item(self, conf.vec(col, row), 'machinegun')
                elif tile == conf.SW_TILE:
                    Item(self, conf.vec(col, row), 'shockwave')
                elif tile == conf.SG_TILE:
                    Item(self, conf.vec(col, row), 'shotgun')
        for row, tiles in enumerate(self.maps[self.map_progress].data):
            for col, tile in enumerate(tiles):
                if tile == conf.MOB_TILE:
                    Mob(self, conf.vec(col, row))

        self.paused = False

        self.camera = Camera(self, self.maps[self.map_progress].width, self.maps[self.map_progress].height)
        self.background = Background(self, conf.vec(
            self.maps[self.map_progress].width / 4, self.maps[self.map_progress].height / 4))
        self.soundManager.play_sound_effect(self.effect_sounds['level_start'])

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.soundManager.play_music()

        while self.playing:
            self.dt = self.clock.tick(conf.FPS) / 1000.0
            self.events()
            if not self.paused:
                self.update()
            self.screenManager.draw_info(
                conf.BGCOLOR,
                self.title_font,
                self.player.health,
                self.clock.get_fps(),
                self.points + self.player.points_current_level,
                self.player.secondary_weapon_bullets,
                self.player.secondary_weapon
                )

    def quit(self):
        pg.quit()
        #TODO sys.exit()??

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_m:
                    self.soundManager.toggle_mute()
                if event.key == pg.K_r:
                    self.new()
                    self.run()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_SPACE and len(self.mobs) == 0:
                    self.add_points(self.player.points_current_level)
                    self.player_health = self.player.health
                    if self.map_progress < len(self.maps) - 1:
                        self.map_progress += 1
                    else:
                        self.map_progress = 0
                    self.new()
                    self.run()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def add_points(self, pointsToAdd):
        self.points += pointsToAdd
