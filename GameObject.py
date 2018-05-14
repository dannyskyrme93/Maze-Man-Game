import pyglet


class GameObject:
    PREFIX = "img\\"
    POSTFIX = ".png"

    def __init__(self, posx, posy, filename=None):
        self.filename = filename
        self.posx = posx
        self.posy = posy
        if filename is not None:
            self.image = None
            self.update_image()

    def get_image(self):
        return self.image

    def update_image(self):
        self.image = pyglet.image.load(GameObject.PREFIX + self.filename +
                                       GameObject.POSTFIX)


