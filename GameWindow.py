import pyglet
import pyglet.window
from pyglet.window import key
from SoundBase import SoundBase as SB
from Model import Model
from RegionModel import RegionModel
import math


class GameWindow(pyglet.window.Window):
    ADJ_CONSTANT = 0.25
    SQUARE_SIZE = 25
    GLOW_COLOUR_ARR = (255, 215, 0)
    WIDTH_IN_SQUARES = 80
    HEIGHT_IN_SQUARES = 40
    vertex_list = None
    tick = 0
    edge_list = []

    def __init__(self):
        super().__init__()
        self.fps_display = pyglet.clock.ClockDisplay()
        self.set_location(10, 30)
        self.model = Model(GameWindow.WIDTH_IN_SQUARES, GameWindow.HEIGHT_IN_SQUARES)
        self.set_size(GameWindow.WIDTH_IN_SQUARES * GameWindow.SQUARE_SIZE, GameWindow.HEIGHT_IN_SQUARES * GameWindow.SQUARE_SIZE)
        self.sprite = pyglet.sprite.Sprite(self.model.sprite_obj.get_image())
        self.sprite.scale = (GameWindow.SQUARE_SIZE - 1) / self.sprite.width
        self.objs = {}
        self.update_edge_list()
        self.update_vertex_list()
        self.sounds = SB()
        self.glow_batch = None
        self.glow_colours = []
        for x in range(0, RegionModel.GLOW_TRAIL):
            y = (RegionModel.GLOW_TRAIL - x) / RegionModel.GLOW_TRAIL
            self.glow_colours += [int(GameWindow.GLOW_COLOUR_ARR[c] * y) for c in range(0, 3)]

    def on_draw(self):
        self.clear()
        square_size = self.SQUARE_SIZE
        if not self.model.reg_model.glow_pts == []:
            self.glow_batch = pyglet.graphics.Batch()
            arr = self.model.reg_model.get_current_points()
            for x in range(0, min(len(arr), RegionModel.GLOW_TRAIL)):
                group = arr[x]
                print("Group: ", group)
                num_of = math.ceil(len(group))
                glow_vertex_list = []
                print(self.glow_colours)
                print(self.glow_colours[x*3:x*3+3])
                print(len(self.glow_colours))
                print(x*3, x*3+3)
                glow_colour_list = tuple(self.glow_colours[x*3:x*3+3] * (num_of * 4))
                for xy in group:
                    x, y = xy[0] * square_size, xy[1] * square_size
                    dx = x + square_size
                    dy = y + square_size
                    in_pts = [x, y, dx, y, dx, dy, x, dy]
                    glow_vertex_list = glow_vertex_list + in_pts
                glow_vertex_list = tuple(glow_vertex_list)
                print(glow_vertex_list, len(glow_vertex_list) / 2, sep="|")
                print(glow_colour_list, len(glow_colour_list) / 3, sep="|")
                print("$", (4*num_of))
                self.glow_batch.add(4 * num_of, pyglet.gl.GL_QUADS, None, ('v2i', glow_vertex_list),
                                    ('c3B', glow_colour_list))
            self.glow_batch.draw()
        self.glow_batch = pyglet.graphics.Batch()
        self.vertex_list.draw(pyglet.gl.GL_LINES)
        for obj in self.model.objects.values():
            current_sprite = pyglet.sprite.Sprite(obj.get_image())
            current_sprite.x = obj.posx * square_size
            current_sprite.y = obj.posy * square_size
            current_sprite.scale = (GameWindow.SQUARE_SIZE - 1) / current_sprite.width
            current_sprite.draw()
        self.sprite.draw()
        self.fps_display.draw()

    def pre_render_glow(self):
        pass

    def update_vertex_list(self):
        temp = []
        square_size = GameWindow.SQUARE_SIZE
        for y in range(0, GameWindow.HEIGHT_IN_SQUARES):
            for x in range(0, GameWindow.WIDTH_IN_SQUARES):
                index = y * GameWindow.WIDTH_IN_SQUARES + x % GameWindow.WIDTH_IN_SQUARES
                temp.append(x * square_size)
                temp.append(y * square_size)
        total_pts = GameWindow.WIDTH_IN_SQUARES * GameWindow.HEIGHT_IN_SQUARES
        self.vertex_list = pyglet.graphics.vertex_list_indexed(total_pts, self.edge_list, ('v2i', tuple(temp)))

    def update_edge_list(self):
        self.edge_list = []
        for y in range(0, GameWindow.HEIGHT_IN_SQUARES-1):
            for x in range(0, GameWindow.WIDTH_IN_SQUARES-1):
                root_index = y * GameWindow.WIDTH_IN_SQUARES + x % GameWindow.WIDTH_IN_SQUARES
                if self.model.horz[y][x]:
                    self.edge_list.append(root_index)
                    self.edge_list.append(root_index + 1)
                if self.model.vert[y][x]:
                    self.edge_list.append(root_index)
                    self.edge_list.append(root_index + GameWindow.WIDTH_IN_SQUARES)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.MOTION_UP:
            self.model.sprite_obj.vely = 0
        elif symbol == key.MOTION_DOWN:
            self.model.sprite_obj.vely = 0
        elif symbol == key.MOTION_LEFT:
            self.model.sprite_obj.velx = 0
        elif symbol == key.MOTION_RIGHT:
            self.model.sprite_obj.velx = 0
        elif symbol == key.SPACE:
            self.model.break_line()
            self.update_edge_list()
            self.update_vertex_list()
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.MOTION_UP:
            self.model.sprite_obj.vely = 1
            self.model.sprite_obj.dir = 0
        elif symbol == key.MOTION_DOWN:
            self.model.sprite_obj.vely = - 1
            self.model.sprite_obj.dir = 2
        elif symbol == key.MOTION_LEFT:
            self.model.sprite_obj.velx = - 1
            self.model.sprite_obj.dir = 3
        elif symbol == key.MOTION_RIGHT:
            self.model.sprite_obj.velx = 1
            self.model.sprite_obj.dir = 1
        elif symbol == key.SPACE:
            self.model.sprite_obj.charge_it()
            self.sounds.play_sound('wood')
        self.model.sprite_obj.update_image()
        self.sprite.image = self.model.sprite_obj.image
        pass

    def update(self, dt):
        square_size = GameWindow.SQUARE_SIZE
        if self.tick % 3 == 0:
            self.model.update(dt)

        self.sprite.x = self.sprite.x + \
                        GameWindow.ADJ_CONSTANT * (self.model.sprite_obj.posx * square_size - self.sprite.x)

        self.sprite.y = self.sprite.y + \
                        GameWindow.ADJ_CONSTANT * (self.model.sprite_obj.posy * square_size - self.sprite.y)
        self.tick += 1
        if self.model.sprite_obj.is_charging():
            self.model.sprite_obj.charge_it()

