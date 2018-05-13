import pyglet


class GameObject:
    PREFIX = "img\\"
    POSTFIX = ".png"
    threshold = 10

    def __init__(self, posx, posy, filename):
        self.filename = filename
        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0
        self.dir = 0
        self.image = None
        self.update_image()
        self.walk_vel = 5
        self.charge = 0

    def get_image(self):
        return self.image

    def update_image(self):
        self.image = pyglet.image.load(GameObject.PREFIX + self.filename + self.get_file_direction() +
                                       GameObject.POSTFIX)

    def get_file_direction(self):
        if self.dir == 0:
            return "Up"
        elif self.dir == 1:
            return "Right"
        elif self.dir == 2:
            return "Down"
        else:
            return "Left"

    def charge_it(self):
        self.charge += 1

    def is_charged(self):
        return self.charge > GameObject.threshold

    def discharge_it(self):
        self.charge = 0

    def is_charging(self):
        return self.charge > 0
