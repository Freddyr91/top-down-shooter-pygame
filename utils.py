import settings as conf
from map import Map
from os import path
import pygame as pg

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
        print(one.hit_rect, two.hit_rect)
        return one.hit_rect.colliderect(two.hit_rect)
    return one.hit_rect.colliderect(two.rect)

def load_files_in_folder(filenames, folder, filetype):
    if type(filenames) is dict:
        loaded_files = {}
        for i in filenames:
            loaded_files[i] = []
            if type(filenames[i]) is list:
                for file in filenames[i]:
                    loaded_files[i].append(load_single_file(folder, file, filetype))
            elif type(i) is str:
                loaded_files[i] = load_single_file(folder, filenames[i], filetype)
        return loaded_files
    if type(filenames) is list:
        loaded_files = []
        for file in filenames:
            loaded_files.append(load_single_file(folder, file, filetype))
        return loaded_files
    if type(filenames) is str:
        return load_single_file(folder, filenames, filetype)
    return None

def load_single_file(folder, filename, filetype):
    if (filetype == 'sound'):
        s = pg.mixer.Sound(path.join(folder,filename))
        s.set_volume(0.1)
        return s
    elif (filetype == 'image'):
        return pg.image.load(path.join(folder, filename)).convert_alpha()
    else:
        print('file ' + filename + " of type " + filetype + " was not found in folder " + folder)
        return None

def load_sounds_in_folder(filenames, folder):
    return load_files_in_folder(filenames, folder, 'sound')

def load_images_in_folder(filenames, folder):
    return load_files_in_folder(filenames, folder, 'image')

def load_maps(folder):
    maps = []
    for map_filename in conf.MAPS:
        maps.append(Map(path.join(folder, map_filename)))
    return maps

def rotate_image(image, angle):
    rot_image = conf.pg.transform.rotate(image, angle)
    return rot_image
