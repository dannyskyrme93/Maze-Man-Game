import pyglet
import GameObject
from Action import Action
from Agent import Agent
from GameObject import GameObject

class LiveObject(GameObject):
    ENEMY_VEL = 5
    threshold = 10

    def __init__(self, posx, posy, filename, is_agent=False):
        super().__init__(posx, posy)
        self.velx = 0
        self.vely = 0
        self.walk_vel = 5
        self.charge = 0
        self.direction = 0
        self.filename = filename
        self.image = None
        self.update_image()

        if is_agent:
            self.agent = Agent()
            self.walk_vel = 1

    def charge_it(self):
        self.charge += 1

    def is_charged(self):
        return self.charge > LiveObject.threshold

    def discharge_it(self):
        self.charge = 0

    def is_charging(self):
        return self.charge > 0

    def get_file_direction(self):
        if self.direction == 0:
            return "Up"
        elif self.direction == 1:
            return "Right"
        elif self.direction == 2:
            return "Down"
        else:
            return "Left"

    def update_image(self):
        self.image = pyglet.image.load(LiveObject.PREFIX + self.filename + self.get_file_direction() +
                                       LiveObject.POSTFIX)

    def action(self, model):
        self.direction = self.agent.action(model, self)
        if self.direction == Action.UP_MOVE:
            self.vely = self.walk_vel
        elif self.direction == Action.RIGHT_MOVE:
            self.velx = self.walk_vel
        elif self.direction == Action.DOWN_MOVE:
            self.vely = - self.walk_vel
        else:
            self.velx = - self.walk_vel
        self.update_image()
