import random as ran
from LiveObject import LiveObject
from GameObject import GameObject
import random as rand

class Model:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        Model.vert, Model.horz = self.build_line_table()
        self.objects = {}
        self.charge = 0
        self.sprite_obj = LiveObject(20, 20, "sprite")
        self.add_pick_ups(8)

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
        self.collisions()

    def collisions(self):
        objs = self.objects.copy()
        for id in objs:
            obj = self.objects[id]
            val = (obj.posx, obj.posy)
            if (self.sprite_obj.posx, self.sprite_obj.posy) == val:
                del self.objects[id]
                self.add_pick_ups(1)

    def add_pick_ups(self, num_of):
        for x in range(0, num_of):
            self.objects[rand.getrandbits(16)] = \
            GameObject(rand.randint(0, self.width), rand.randint(0, self.height), "Pickup")

