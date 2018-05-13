import random as ran
from GameObject import GameObject

class Model:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        Model.vert, Model.horz = self.build_line_table()
        self.sprite_obj = GameObject(20, 20, "sprite")
        self.charge = 0

    def build_line_table(self):
        vert = [[bool(ran.randint(0, 1)) for x in range(0, self.width-1)]
                for y in range(0, self.height)]
        horz = [[bool(ran.randint(0, 1)) for x in range(0, self.width-1)]
                for y in range(0, self.height)]
        return vert, horz

    def break_line(self):
        if self.sprite_obj.is_charged():
            d = self.sprite_obj.dir
            if d == 0:
                Model.horz[self.sprite_obj.posy + 1][self.sprite_obj.posx] = False
            elif d == 1:
                Model.vert[self.sprite_obj.posy][self.sprite_obj.posx + 1] = False
            elif d == 2:
                Model.horz[self.sprite_obj.posy][self.sprite_obj.posx] = False
            else:
                Model.vert[self.sprite_obj.posy][self.sprite_obj.posx] = False

            self.sprite_obj.discharge_it

    def update(self):
        if self.sprite_obj.velx > 0 and \
                not Model.vert[self.sprite_obj.posy ][self.sprite_obj.posx + 1] \
                and self.sprite_obj.posx < self.width - 4:
            self.sprite_obj.posx += self.sprite_obj.velx
        if self.sprite_obj.velx < 0 and \
                not Model.vert[self.sprite_obj.posy][self.sprite_obj.posx] \
                and self.sprite_obj.posx > 0:
            self.sprite_obj.posx += self.sprite_obj.velx
        if self.sprite_obj.vely > 0 and not Model.horz[self.sprite_obj.posy + 1][self.sprite_obj.posx] \
                and self.sprite_obj.posy < (self.height - 2):
            self.sprite_obj.posy += self.sprite_obj.vely
        if self.sprite_obj.vely < 0 and not Model.horz[self.sprite_obj.posy][self.sprite_obj.posx] \
                and self.sprite_obj.posy > 0:
            self.sprite_obj.posy += self.sprite_obj.vely



