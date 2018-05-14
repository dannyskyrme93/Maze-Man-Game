import pyglet
import pyglet.window
from pyglet.window import key
from SoundBase import SoundBase as SB
from Model import Model


class GameWindow(pyglet.window.Window):
    ADJ_CONSTANT = 0.25
    SQUARE_SIZE = 25
    WIDTH_IN_SQUARES = 80
    HEIGHT_IN_SQUARES = 40
    vertex_list = None
    tick = 0
    edge_list = []

    def __init__(self):
        super().__init__()
        self.set_location(0, 0)
        self.model = Model(GameWindow.WIDTH_IN_SQUARES, GameWindow.HEIGHT_IN_SQUARES)
        self.set_size(GameWindow.WIDTH_IN_SQUARES * GameWindow.SQUARE_SIZE, GameWindow.HEIGHT_IN_SQUARES * GameWindow.SQUARE_SIZE)
        self.sprite = pyglet.sprite.Sprite(self.model.sprite_obj.get_image())
        self.sprite.scale = (GameWindow.SQUARE_SIZE - 1) / self.sprite.width
        self.update_edge_list()
        self.update_vertex_list()
        self.sounds = SB()

    def on_draw(self):
        self.clear()
        self.vertex_list.draw(pyglet.gl.GL_LINES)
        self.sprite.draw()

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
        print(self.vertex_list.vertices[100])

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
        print(self.edge_list)

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
            self.model.update()
        self.sprite.x = self.sprite.x + GameWindow.ADJ_CONSTANT * (self.model.sprite_obj.posx * square_size - self.sprite.x)
        self.sprite.y = self.sprite.y + GameWindow.ADJ_CONSTANT * (self.model.sprite_obj.posy * square_size - self.sprite.y)
        self.tick += 1
        if self.model.sprite_obj.is_charging():
            self.model.sprite_obj.charge_it()

