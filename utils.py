from settings import *

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_hit_rect(one, two):
    if hasattr(two, "hit_rect") and hasattr(two, "type"):
        print (one.hit_rect, two.hit_rect)
        return one.hit_rect.colliderect(two.hit_rect)
    return one.hit_rect.colliderect(two.rect)

#HUD
def draw_player_health(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = health/100.0 * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if health > PLAYER_HEALTH * 0.6:
        col = GREEN
    elif health > PLAYER_HEALTH * 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

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

def load_files_in_folder(filenames, folder, filetype):
    if type(filenames) is dict:
        loaded_files = {}
        for i in filenames:
            loaded_files[i] = []
            if type(filenames[i]) is list:
                for file in filenames[i]:
                    if (filetype == 'sound'):
                        s = pg.mixer.Sound(path.join(folder, file))
                        s.set_volume(0.1)
                        loaded_files[i].append(s)
                    if (filetype == 'image'):
                        loaded_files[i].append(pg.image.load(path.join(folder, file)).convert_alpha())
            elif type(i) is str:
                if (filetype == 'sound'):
                    s = pg.mixer.Sound(path.join(folder, filenames[i]))
                    s.set_volume(0.1)
                    loaded_files[i] = s
                if (filetype == 'image'):
                    loaded_files[i] = pg.image.load(path.join(folder, filenames[i])).convert_alpha()
        return loaded_files
    if type(filenames) is list:
        loaded_files = []
        for file in filenames:
            if (filetype == 'sound'):
                s = pg.mixer.Sound(path.join(folder, file))
                s.set_volume(0.1)
                loaded_files.append(s)
            elif (filetype == 'image'):
                loaded_files.append(pg.image.load(path.join(folder, file)).convert_alpha())
        return loaded_files
    if type(filenames) is str:
        file = None
        if filetype == 'sound':
            s = pg.mixer.Sound(path.join(folder, filenames))
            s.set_volume(0.1)
            file = s
        elif filetype == 'image':
            file = pg.image.load(path.join(folder, filenames)).convert_alpha()
        return file
    return None

def load_sounds_in_folder(filenames, folder):
    return load_files_in_folder(filenames, folder, 'sound')

def load_images_in_folder(filenames, folder):
    return load_files_in_folder(filenames, folder, 'image')