import GameObject
import pyglet


class LiveObject(GameObject.GameObject):
    threshold = 10

    def __init__(self, posx, posy, filename):
        super().__init__(posx, posy)
        self.velx = 0
        self.vely = 0
        self.walk_vel = 5
        self.charge = 0
        self.dir = 0
        if filename is not None:
            self.filename = filename
            self.image = None
            self.update_image()

    def charge_it(self):
        self.charge += 1

    def is_charged(self):
        return self.charge > LiveObject.threshold

    def discharge_it(self):
        self.charge = 0

    def is_charging(self):
        return self.charge > 0

    def get_file_direction(self):
        if self.dir == 0:
            return "Up"
        elif self.dir == 1:
            return "Right"
        elif self.dir == 2:
            return "Down"
        else:
            return "Left"

    def update_image(self):
        self.image = pyglet.image.load(LiveObject.PREFIX + self.filename + self.get_file_direction() +
                                       LiveObject.POSTFIX)