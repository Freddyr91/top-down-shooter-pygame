from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def mouseadjustment(self, mouse):
        return vec(mouse) + vec(-self.camera.left, -self.camera.top)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        #TODO move camera according to mouse position
        #mouse_dir = vec(self.mouseadjustment(pg.mouse.get_pos())) - vec(target.pos)
        #mouse_mag = mouse_dir.length() / 10

        # limit scolling to map size
        x = min(0, x) #left
        y = min(0, y) #top
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        #y = max(WIDTH/TILESIZE, y)
        self.camera = pg.Rect(x, y, self.width, self.height)
