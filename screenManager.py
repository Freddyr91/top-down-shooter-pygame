from settings import *
import pygame as pg
import settings as conf

class ScreenManager():
    def __init__(self, game):
        self.game = game

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(self.game.asset_folder + "/" + font_name, size)
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
        self.game.screen.blit(text_surface, text_rect)

    def draw_player_health(self, surf, x, y, health):
        if health < 0:
            health = 0
        conf.BAR_LENGTH = 100
        conf.BAR_HEIGHT = 20
        fill = health / 100.0 * conf.BAR_LENGTH
        outline_rect = pg.Rect(x, y, conf.BAR_LENGTH, conf.BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, conf.BAR_HEIGHT)
        if health > conf.PLAYER_HEALTH * 0.6:
            col = conf.GREEN
        elif health > conf.PLAYER_HEALTH * 0.3:
            col = conf.YELLOW
        else:
            col = conf.RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, conf.WHITE, outline_rect, 2)

    def draw_info(self, bg_color, font, player_health, fps, points, secondary_bullets, secondary_weapon):
        self.game.screen.fill(bg_color)
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.game.camera.apply(sprite))

        #HUD
        self.draw_player_health(self.game.screen, 10, 10, player_health)
        self.draw_text('FPS ' + '{:.2f}'.format(fps),
                        font, conf.DEFAULT_FONT_SIZE, conf.WHITE, 120, 10, align='nw')
        self.draw_text('Points ' + '{}'.format(points),
                        font, conf.DEFAULT_FONT_SIZE, conf.WHITE, 10, conf.HEIGHT - 10, align='sw')
        if (secondary_bullets > 0):
            self.draw_text('Secondary weapon: {} | ammo:{: 3d}'.format(secondary_weapon,
                            secondary_bullets), 
                            font, 24, conf.WHITE, conf.WIDTH - 10, conf.HEIGHT - 10, align='se')
        if self.game.paused:
            self.game.screen.blit(self.game.dim_screen_img, (0, 0))
            self.draw_text('Paused', font, 105, conf.RED, conf.WIDTH / 2, conf.HEIGHT / 2, 'center')
            self.draw_text('Press P to unpause game', font,
                            conf.DEFAULT_FONT_SIZE, conf.WHITE, conf.WIDTH, 0, 'ne')
            self.draw_text('Press M to toggle mute', font,
                            conf.DEFAULT_FONT_SIZE, conf.WHITE, conf.WIDTH, 24, 'ne')
            self.draw_text('Press R to restart game', font,
                            conf.DEFAULT_FONT_SIZE, conf.WHITE, conf.WIDTH, 48, 'ne')
        else:
            self.draw_text('Press P to pause game', font,
                            conf.DEFAULT_FONT_SIZE, conf.WHITE, conf.WIDTH - 10, 10, 'ne')
        if len(self.game.mobs) == 0:
            self.draw_text('No more enemies', font, 64,
                            conf.GREEN2, conf.WIDTH / 2, conf.HEIGHT / 4, 'center')
            self.draw_text('Press Space to go to next level', font, 64,
                            conf.WHITE, conf.WIDTH / 2, conf.HEIGHT / 4 + 70, 'center')
        pg.display.flip()
