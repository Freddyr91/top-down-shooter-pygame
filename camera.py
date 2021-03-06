import settings as conf

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera = conf.pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        if (entity == self.game.background):
            return entity.rect.move(self.camera.x*0.5, self.camera.y*0.5) # parallax scrolling on background
        return entity.rect.move(self.camera.topleft)

    def mouseadjustment(self, mouse):
        return conf.vec(mouse) + conf.vec(-self.camera.left, -self.camera.top)

    def update(self, target):
        x = -target.rect.centerx + int(conf.WIDTH / 2)
        y = -target.rect.centery + int(conf.HEIGHT / 2)

        #TODO move camera according to mouse position
        #mouse_dir = conf.vec(self.mouseadjustment(conf.pg.mouse.get_pos())) - conf.vec(target.pos)
        #mouse_mag = mouse_dir.length() / 10

        # limit scolling to map size
        x = min(0, x) #left
        y = min(0, y) #top
        x = max(-(self.width - conf.WIDTH), x)
        y = max(-(self.height - conf.HEIGHT), y)
        self.camera = conf.pg.Rect(x, y, self.width, self.height)
