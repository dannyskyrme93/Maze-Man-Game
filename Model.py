import random as ran
from LiveObject import LiveObject
from GameObject import GameObject
import random as rand
import RegionModel as rm

class Model:

    DISCONNECT = 0.4

    def __init__(self, w, h):
        self.width = w
        self.height = h
        Model.vert, Model.horz = self.build_line_table()
        self.reg_model = rm.RegionModel(Model.vert, Model.horz)
        self.objects = {}
        self.charge = 0
        self.sprite_obj = LiveObject(0, 0, "sprite")
        self.add_pick_ups(8)
        self.glow_changed = False

    def build_line_table(self):
        vert = [[(rand.random() > Model.DISCONNECT) for x in range(0, self.width-1)]
                for y in range(0, self.height-1)]
        horz = [[(rand.random() > Model.DISCONNECT) for x in range(0, self.width-1)]
                for y in range(0, self.height-1)]
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
            self.reg_model.fill_ids(self.vert, self.horz)
            self.reg_model.clear_glow()
            self.reg_model.trigger_glow(self.sprite_obj.posx, self.sprite_obj.posy)
            self.glow_changed = True

    def update(self, dt):
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
        self.reg_model.update_glow()

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

    def is_glow_changed(self):
        if self.glow_changed:
            self.glow_changed = False
            return True
        return False