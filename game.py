from settings import *
from map import *
import environment
from camera import *
from item import *
from player import *
from mob import *
from soundManager import SoundManager

class Game:
    def __init__(self):
        self.soundManager = SoundManager()
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
        self.player_img = load_images_in_folder(PLAYER_IMG, img_folder)
        self.wall_img = load_images_in_folder(WALL_IMG, img_folder)
        self.bullet_imgs = load_images_in_folder(BULLET_IMGS, img_folder)
        self.noise_imgs = load_images_in_folder(NOISE_IMGS, img_folder)
        self.floor_imgs = load_images_in_folder(FLOOR_IMGS, img_folder)
        self.flash_imgs = load_images_in_folder(BULLET_FLASH_IMGS, img_folder)
        self.item_imgs = load_images_in_folder(ITEM_IMGS, img_folder)
        self.splat_imgs = load_images_in_folder(SPLAT_IMGS, img_folder)
        # Sound
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effect_sounds = load_sounds_in_folder(EFFECTS_SOUNDS, snd_folder)
        self.weapon_sounds = load_sounds_in_folder(WEAPON_SOUNDS, snd_folder)
        self.enemy_sounds = load_sounds_in_folder(ENEMY_SOUNDS, snd_folder)
        for s in self.enemy_sounds:
            s.set_volume(.2)
        self.player_hit_sounds = load_sounds_in_folder(PLAYER_HIT_SOUNDS, snd_folder)
        ## TODO - Found other sound for this
        self.enemy_hit_sounds = load_sounds_in_folder(ENEMY_SOUNDS, snd_folder)
        for s in self.enemy_hit_sounds:
            s.set_volume(.2)
            

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                environment.Floor(self, vec(col, row))
                if tile == '1':
                    environment.Wall(self, vec(col, row))
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
        self.soundManager.play_sound_effect(self.effect_sounds['level_start'])

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.soundManager.play_music()

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
                self.soundManager.play_sound_effect(self.effect_sounds['health_up'])
                self.player.add_health(ITEM_HEALTH_AMOUNT)
        # mob hits
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                self.soundManager.play_sound_effect(choice(self.player_hit_sounds))
                
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
        draw_text(self, "FPS " + "{:.2f}".format(self.clock.get_fps()), self.title_font, 24, WHITE, 120, 10, align = "nw")
        if self.paused:
            self.screen.blit(self.dim_screen_img, (0,0))
            draw_text(self, "Paused", self.title_font, 105, RED, WIDTH/2, HEIGHT/2, align = "center")
            draw_text(self, "Press P to unpause game", self.title_font, 24, WHITE, WIDTH, 0, align = "ne")
            draw_text(self, "Press M to toggle mute", self.title_font, 24, WHITE, WIDTH, 24, align = "ne")
            draw_text(self, "Press R to restart game", self.title_font, 24, WHITE, WIDTH, 48, align = "ne")
        else:
            draw_text(self, "Press P to pause game", self.title_font, 24, WHITE, WIDTH, 0, align = "ne")
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
            elif event.type == pg.KEYUP:
                if event.key == pg.K_m:
                    self.soundManager.toggle_mute()
                if event.key == pg.K_r:
                    self.new()
                    self.run()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass