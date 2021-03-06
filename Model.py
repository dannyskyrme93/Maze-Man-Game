import random as ran
from LiveObject import LiveObject
from GameObject import GameObject
import random as rand
import RegionModel as rm
from Action import Action
from Percept import  Percept

class Model:

    DISCONNECT = 0.45
    NUM_OF_ENEMIES = 1
    ID_LENGTH_IN_BITS = 16

    def __init__(self, w, h):
        self.width = w
        self.height = h
        Model.vert, Model.horz = self.build_line_table()
        self.reg_model = rm.RegionModel(Model.vert, Model.horz)
        Model.vert, Model.horz = self.reg_model.remove_superfluous_lines()
        self.pick_ups = {}
        self.charge = 0
        self.sprite_obj = LiveObject(self.width // 2, self.height // 2, "Sprite")
        self.add_pick_ups(8)
        self.glow_changed = False
        self.enemies = {}
        self.add_npcs()

    def build_line_table(self):
        vert = [[(rand.random() > Model.DISCONNECT) for x in range(0, self.width-1)]
                for y in range(0, self.height-1)]
        horz = [[(rand.random() > Model.DISCONNECT) for x in range(0, self.width-1)]
                for y in range(0, self.height-1)]
        return vert, horz

    def break_line(self):
        if self.sprite_obj.is_charged():
            d = self.sprite_obj.direction
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
            self.sprite_obj.direction = 3
        if self.sprite_obj.vely > 0 and not Model.horz[self.sprite_obj.posy + 1][self.sprite_obj.posx] \
                and self.sprite_obj.posy < (self.height - 3):
            self.sprite_obj.posy += self.sprite_obj.vely
        if self.sprite_obj.vely < 0 and not Model.horz[self.sprite_obj.posy][self.sprite_obj.posx] \
                and self.sprite_obj.posy > 0:
            self.sprite_obj.posy += self.sprite_obj.vely
        for enemy in self.enemies.values():
            per = Percept(self, enemy.posx, enemy.posy, 100)
            enemy.action(per)
        self.update_enemies()
        self.collisions()
        self.reg_model.update_glow()

    def update_enemies(self):
        for enemy in self.enemies.values():
            if enemy.velx > 0 and \
                    not Model.vert[enemy.posy][enemy.posx + 1] \
                    and enemy.posx < self.width - 4:
                enemy.posx += enemy.velx
            if enemy.velx < 0 and \
                    not Model.vert[enemy.posy][enemy.posx] \
                    and enemy.posx > 0:
                enemy.posx += enemy.velx
            if enemy.vely > 0 and not Model.horz[enemy.posy + 1][enemy.posx] \
                    and enemy.posy < (self.height - 3):
                enemy.posy += enemy.vely
            if enemy.vely < 0 and not Model.horz[enemy.posy][enemy.posx] \
                    and enemy.posy > 0:
                enemy.posy += enemy.vely

    def collisions(self):
        objs = self.pick_ups.copy()
        for id in objs:
            obj = self.pick_ups[id]
            val = (obj.posx, obj.posy)
            if (self.sprite_obj.posx, self.sprite_obj.posy) == val:
                del self.pick_ups[id]
                self.add_pick_ups(1)

    def add_pick_ups(self, num_of):
        for x in range(0, num_of):
            self.pick_ups[rand.getrandbits(Model.ID_LENGTH_IN_BITS)] = \
            GameObject(rand.randint(0, self.width), rand.randint(0, self.height), "Pickup")

    def add_npcs(self):
        for x in range(0, Model.NUM_OF_ENEMIES):
            eye = ran.getrandbits(Model.ID_LENGTH_IN_BITS)
            self.enemies[eye] = LiveObject(rand.randint(0, self.width-4), rand.randint(0, self.height-4), "Enemy", True)
            self.enemies[eye].walk_vel = 1
        

    def is_glow_changed(self):
        if self.glow_changed:
            self.glow_changed = False
            return True
        return False

    def process_behaviours(self):
        for enemy in self.enemies.values():
            enemy.action()
