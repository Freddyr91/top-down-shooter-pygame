from os import path
import settings as conf
import environment
from camera import *
from item import *
from player import *
from mob import Mob
from soundManager import SoundManager
import utils

class Game:
    def __init__(self):
        self.soundManager = SoundManager()
        # Full-screen test stuff
        #user32 = conf.ctypes.windll.user32
        #screenSize =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        #print(screenSize)
        #size = (screenSize)
        #pg.display.set_mode((size) , pg.FULLSCREEN)
        #pg.display.set_caption(conf.TITLE)
        #conf.WIDTH = screenSize[0]
        #conf.HEIGHT = screenSize[1]
        self.screen = conf.pg.display.set_mode((conf.WIDTH, conf.HEIGHT))
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        pg.mouse.set_cursor(*pg.cursors.broken_x)
        self.map_progress = 0
        self.points = 0

    def load_data(self):
        game_folder = path.dirname('__file__')
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.asset_folder = path.join(game_folder, 'assets')

        self.title_font = path.join(game_folder, conf.FONT)
        self.dim_screen_img = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen_img.fill((0,0,0,120))

        self.maps = utils.load_maps(self.asset_folder)
        self.player_imgs = utils.load_images_in_folder(conf.PLAYER_IMGS, img_folder)
        for i in range (0, len(self.player_imgs)):
            self.player_imgs[i] = pg.transform.scale(self.player_imgs[i], (conf.TILESIZE, conf.TILESIZE))
        self.wall_img = utils.load_images_in_folder(conf.WALL_IMG, img_folder)
        self.bullet_imgs = utils.load_images_in_folder(conf.BULLET_IMGS, img_folder)
        self.noise_imgs = utils.load_images_in_folder(conf.NOISE_IMGS, img_folder)
        self.floor_imgs = utils.load_images_in_folder(conf.FLOOR_IMGS, img_folder)
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
        ## TODO - Find other sound for this
        self.enemy_hit_sounds = utils.load_sounds_in_folder(conf.ENEMY_SOUNDS, snd_folder)
        for s in self.enemy_hit_sounds:
            s.set_volume(.2)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for row, tiles in enumerate(self.maps[self.map_progress].data):
            for col, tile in enumerate(tiles):
                environment.Floor(self, conf.vec(col, row))
                if tile == conf.WALL_TILE:
                    environment.Wall(self, conf.vec(col, row))
                elif tile == conf.PLAYER_TILE:
                    self.player = Player(self, conf.vec(col, row))
                elif tile == conf.HEALTH_TILE:
                    Item(self, conf.vec(col, row), "health")
                elif tile == conf.MG_TILE:
                    Item(self, conf.vec(col, row), "mg_pickup")
                elif tile == conf.SW_TILE:
                    Item(self, conf.vec(col, row), "sw_pickup")
        for row, tiles in enumerate(self.maps[self.map_progress].data):
            for col, tile in enumerate(tiles):
                if tile == conf.MOB_TILE:
                    Mob(self, conf.vec(col, row))

        self.paused = False

        self.camera = Camera(self.maps[self.map_progress].width, self.maps[self.map_progress].height)
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
            self.draw()

    def quit(self):
        pg.quit()
        #sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(conf.BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        #HUD
        utils.draw_player_health(self.screen, 10, 10, self.player.health)
        utils.draw_text(self, "FPS " + "{:.2f}".format(self.clock.get_fps()), self.title_font, 24, conf.WHITE, 120, 10, align = "nw")
        utils.draw_text(self, "Points " + "{}".format(self.points + self.player.points_current_level), self.title_font, 24, conf.WHITE, 10, conf.HEIGHT-10, align = "sw")
        if (self.player.secondary_weapon_bullets > 0):
            utils.draw_text(self, "Secondary weapon -{}- ammo -{}-".format(self.player.secondary_weapon, self.player.secondary_weapon_bullets), self.title_font, 24, conf.WHITE, 10, conf.HEIGHT-34, align = "sw")
        if self.paused:
            self.screen.blit(self.dim_screen_img, (0,0))
            utils.draw_text(self, "Paused", self.title_font, 105, conf.RED, conf.WIDTH/2, conf.HEIGHT/2, "center")
            utils.draw_text(self, "Press P to unpause game", self.title_font, 24, conf.WHITE, conf.WIDTH, 0, "ne")
            utils.draw_text(self, "Press M to toggle mute", self.title_font, 24, conf.WHITE, conf.WIDTH, 24, "ne")
            utils.draw_text(self, "Press R to restart game", self.title_font, 24, conf.WHITE, conf.WIDTH, 48, "ne")
        else:
            utils.draw_text(self, "Press P to pause game", self.title_font, 24, conf.WHITE, conf.WIDTH, 0, "ne")
        if len(self.mobs) == 0:
            utils.draw_text(self, "No more enemies", self.title_font, 64, conf.GREEN2, conf.WIDTH/2, conf.HEIGHT/4, "center")
            utils.draw_text(self, "Press Space to go to next level", self.title_font, 64, conf.WHITE, conf.WIDTH/2, conf.HEIGHT/4+70, "center")
        pg.display.flip()


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
