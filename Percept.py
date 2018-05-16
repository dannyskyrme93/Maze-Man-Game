import math
import random as ran

class Percept:

    def __init__(self, model, center_x, center_y, extent):
        self.target_locations = []
        self.center_x = center_x
        self.center_y = center_y
        self.__set_relative_targets(model, extent)

    def __set_relative_targets(self, model, extent):
        self.reduced =  [[-1 for x in range(0, extent)] for y in range(0, extent)]
        for y in range(self.center_y - extent, self.center_y + extent):
            for x in range(self.center_x - extent, self.center_x + extent):
                if model.sprite_obj.posx == x and model.sprite_obj.posy == y:
                    self.target_locations.append((x, y))
                    print('target found')

    def get_direction(self):
        if len(self.target_locations) == 0:
            print('no target')
            return ran.randint(0, 4)
        x2, y2 = self.target_locations[0]
        dx, dy = self.center_x - x2, self.center_y - y2
        return int(round(4 * math.acos(dx/dy) / math.pi) % 4)



