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
                    self.target_locations.append((x - self.center_x, y - self.center_y))
                    print('target found')

    # TODO migrate to agent
    def get_direction(self):
        if len(self.target_locations) > 0:
            x, y = self.target_locations[0]
            print("x=",x)
            print("y=",y)
            if y != 0:
                to_rtn = math.atan(x/y) % math.pi
                if x < 0:
                    to_rtn += math.pi
                print("ANGLE: ", to_rtn)
                to_rtn = 4*to_rtn / (2 * math.pi)
                to_rtn = int(round(to_rtn)) % 4
                print("Direction: ", to_rtn)
                return to_rtn
            else:
                if x > 0 :
                    return 1
                elif x < 0:
                    return 3
        print('no target')
        return ran.randint(0, 4)

