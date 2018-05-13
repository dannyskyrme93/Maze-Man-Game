import pyglet
from pyglet.window import key
import GameWindow

def update(dt):
    wind.update(dt)


wind = GameWindow.GameWindow()
keys = key.KeyStateHandler()
wind.push_handlers(keys)

tick = 0

pyglet.clock.schedule_interval(update, 0.05)

pyglet.app.run()

