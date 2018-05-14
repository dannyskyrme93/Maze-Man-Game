import pyglet
from pyglet.window import key
import GameWindow
import LiveObject

def update(dt):
    wind.update(dt)


wind = GameWindow.GameWindow()
keys = key.KeyStateHandler()
wind.push_handlers(keys)

tick = 0
dt = 1.0/40
pyglet.clock.schedule_interval(update, dt)

pyglet.app.run()

