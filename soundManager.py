from settings import *

class SoundManager():
    def __init__(self):
        self.muted = True
        pg.mixer.pre_init(44100, -16, 1, 2048)

    def play_sound_effect(self, sound):
        if not self.muted:
            if (sound.get_num_channels() > 2):
                sound.stop()
            sound.play()

    def play_music(self):
        pg.mixer.music.play(loops=-1)
        if self.muted:
            pg.mixer.music.pause()

    def toggle_mute(self):
        if self.muted:
            pg.mixer.music.unpause()
            self.muted = False
        else:
            pg.mixer.music.pause()
            self.muted = True
