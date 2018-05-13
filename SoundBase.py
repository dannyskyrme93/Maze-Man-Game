import pyglet


class SoundBase:

    def __init__(self):
        self.sounds = {}
        pyglet.options['debug_lib'] = True
        wood_sound = pyglet.media.load('sound\\wood_knock.wav', streaming=False)
        self.sounds.update({'wood':wood_sound})
        self.player = pyglet.media.Player()

    def play_sound(self, name):
            '''
            self.player.queue(self.sounds[name])
            self.player.play()
            '''
