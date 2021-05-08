import pyglet
import Core
import Game


class NewApp(pyglet.window.Window):
	def __init__(self):
		super().__init__()
		Core.bind(self)
		pyglet.clock.schedule_interval(self.update, 1 / 120)
		Game.game_launch()

	@staticmethod
	def launch():
		pyglet.app.run()

	def update(self, tick):
		pass


n = NewApp()
n.set_size(1280, 720)
#n.set_fullscreen(True)
n.set_exclusive_mouse(True)

n.launch()
