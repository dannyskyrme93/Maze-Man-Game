
class RegionModel:
    GLOW_TIME = 20

    def __init__(self, vert, horz):
        self.height = len(vert)
        self.width = len(vert[0])
        self.vert = None
        self.horz = None
        self.reg_map = None
        self.fill_ids(vert, horz)
        self.glow_pts = []
        self.glow = 0

    def fill_ids(self, vert, horz):
        current_id = 0
        self.vert = vert
        self.horz = horz
        self.reg_map = [[-1 for x in range(0, self.width)] for y in range(0, self.height)]
        for y in range(len(vert)):
            for x in range(len(vert[0])):
                if self.reg_map[y][x] == -1:
                    self.flood_fill_id(x, y, current_id)
                    current_id += 1

    def flood_fill_id(self, x, y, id):
        if self.reg_map[y][x] == -1:
            self.reg_map[y][x] = id
            # North
            if y < self.height - 1 and not self.horz[y+1][x]:
                self.flood_fill_id(x, y+1, id)
            # South
            if y > 0 and not self.horz[y][x]:
                self.flood_fill_id(x, y-1, id)
            # East
            if x < self.width - 1 and not self.vert[y][x+1]:
                self.flood_fill_id(x+1, y, id)
            # West
            if x > 0 and not self.vert[y][x]:
                self.flood_fill_id(x-1, y, id)

    def flood_fill_glow(self, origin_x, origin_y,  x, y, eye):
        print("tests")
        print(self.reg_map[y][x])
        print(not (x == origin_x and y == origin_y))
        print((x,y) not in self.glow_pts)
        if self.reg_map[y][x] == eye and not (x == origin_x and y == origin_y) and (x, y) not in self.glow_pts:
            self.glow_pts.append((x, y))
            # North
            if y < self.height - 1 and not self.horz[y+1][x]:
                self.flood_fill_glow(origin_x, origin_y, x, y+1, eye)
            # South
            if y > 0 and not self.horz[y][x]:
                self.flood_fill_glow(origin_x, origin_y, x, y-1, eye)
            # East
            if x < self.width - 1 and not self.vert[y][x+1]:
                self.flood_fill_glow(origin_x, origin_y, x+1, y, eye)
            # West
            if x > 0 and not self.vert[y][x]:
                self.flood_fill_glow(origin_x, origin_y, x-1, y, eye)

    def trigger_glow(self, x, y, direction):
        start_x = x
        start_y = y
        if direction == 0:
            start_y += 1
        elif direction == 1:
            start_x += 1
        elif direction == 2:
            start_y -= 1
        else:
            start_x -= 1

        self.glow = self.GLOW_TIME
        self.glow_pts = []
        eye = self.reg_map[start_y][start_x]
        print(x, y, start_x,start_y, sep='|')
        self.flood_fill_glow(x, y, start_x, start_y, eye)
        print(self.glow_pts)

    def clear_glow(self):
        self.glow_pts = []

    def update_glow(self):
        if self.glow == 1:
            self.clear_glow()
        if self.glow > 0:
            self.glow -= 1


