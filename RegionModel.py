from queue import Queue


class RegionModel:
    GLOW_TRAIL = 30
    GLOW_TIME = 4000
    MAX_DEPTH = 100000

    def __init__(self, vert, horz):
        self.height = len(vert)
        self.width = len(vert[0])
        self.vert = None
        self.horz = None
        self.reg_map = None
        self.fill_ids(vert, horz)
        self.glow_pts = []
        self.glow_index = 0
        self.glow = 0
        self.tick = 0

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

    def flood_fill_glow(self, x, y, eye):
        all_pts = []
        q = Queue()
        q.put((x, y, 0))
        while not q.empty():
            tu = q.get()
            print("from q: ", tu)
            (x, y, depth) = tu
            if depth > RegionModel.MAX_DEPTH:
                break
            if (x, y) not in all_pts:
                if depth >= len(self.glow_pts):
                    self.glow_pts.append([])
                self.glow_pts[depth].append((x, y))
                all_pts.append((x, y))
                all_pts.append((x, y))
                # North
                if y < self.height - 1 and not self.horz[y+1][x] and self.reg_map[y+1][x] == eye and (x, y+1) not in all_pts:
                    q.put((x, y+1, depth + 1))
                # East
                if x < self.width - 1 and not self.vert[y][x + 1] and self.reg_map[y][x+1] == eye and (x+1, y) not in all_pts:
                    q.put((x+1, y, depth + 1))
                # South
                if y > 0 and not self.horz[y][x] and self.reg_map[y-1][x] == eye and (x, y-1) not in all_pts:
                    q.put((x, y - 1, depth + 1))
                # West
                if x > 0 and not self.vert[y][x] and self.reg_map[y][x-1] == eye and (x-1, y) not in all_pts:
                    q.put((x-1, y, depth + 1))

    def trigger_glow(self, x, y):
        self.tick = 0
        self.clear_glow()
        self.glow_index = 0
        self.glow = RegionModel.GLOW_TRAIL
        eye = self.reg_map[y][x]
        self.flood_fill_glow(x, y, eye)

        print("The points ", self.glow_pts)

    def clear_glow(self):
        self.glow_pts = []
        self.glow_index = 0

    def update_glow(self):
        if self.tick % RegionModel.GLOW_TIME:
            self.tick += 1
            if self.glow_index == 1:
                self.clear_glow()
            else:
                self.glow -= 1

    def get_current_points(self):
        self.update_glow()
        if not self.glow_pts == []:
            start_index = max(0, self.glow_index - self.GLOW_TRAIL)
            pts = self.glow_pts[start_index:self.glow_index + 1]
            self.glow_index += 1
            return pts
        else:
            return []

    def remove_superfluous_lines(self):
        print(self.width, self.height, sep='|')
        for y in range(0, self.height):
            for x in range(0, self.width):
                val = self.reg_map[y][x]
                # North
                if y < self.height - 1 and self.reg_map[y+1][x] == val:
                    self.horz[y+1][x] = False
                # South
                if y > 0 and self.reg_map[y-1][x] == val:
                    self.horz[y][x] = False
                # East
                if x < self.width - 1 and self.reg_map[y][x+1] == val:
                    self.vert[y][x + 1] = False
                # West
                if y > 0 - 1 and self.reg_map[y][x-1] == val:
                    self.vert[y][x] = False
        return self.vert, self.horz

    '''
        def flood_fill_glow(self, x, y, eye, depth):
        all_pts = [j for i in self.glow_pts for j in i]
        if self.reg_map[y][x] == eye and ((x, y) not in all_pts):
            if depth >= len(self.glow_pts):
                self.glow_pts.append([])
            self.glow_pts[depth].append((x, y))
            # North
            if y < self.height - 1 and not self.horz[y+1][x]:
                self.flood_fill_glow(x, y+1, eye, depth + 1)
            # East
            if x < self.width - 1 and not self.vert[y][x + 1]:
                self.flood_fill_glow(x + 1, y, eye, depth + 1)
            # South
            if y > 0 and not self.horz[y][x]:
                self.flood_fill_glow(x, y-1, eye, depth + 1)
            # West
            if x > 0 and not self.vert[y][x]:
                self.flood_fill_glow(x-1, y, eye, depth + 1)
    '''
