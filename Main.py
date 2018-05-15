import pyglet
from pyglet.window import key
import GameWindow
import LiveObject

def update(dt):
    g_window.update(dt)


g_window = GameWindow.GameWindow()
keys = key.KeyStateHandler()
g_window.push_handlers(keys)
context = g_window.context
tick = 0
dt = 1.0/40
pyglet.clock.set_fps_limit(90)
pyglet.clock.schedule_interval(update, dt)

pyglet.app.run()

