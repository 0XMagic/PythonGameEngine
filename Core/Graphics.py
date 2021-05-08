from pyglet.gl import *
from pywavefront import visualization


#wavefront object


class Model:
	def __init__(self, data):
		self.pos = [0, 0, 0]
		self.rot = [0, 0, 0]
		self.scale = [1, 1, 1]
		self.data = data
		self.t = 0

	#TODO: replace the glRotatef chain for euler angles to a single glRotatef for proper rotation vectors
	def draw(self):
		self.t += 1
		glTranslatef(*self.pos)
		glRotatef(self.rot[0], 1, 0, 0)
		glRotatef(self.rot[1], 0, 1, 0)
		glRotatef(self.rot[2], 0, 0, 1)

		glScalef(*self.scale)
		for d in self.data:
			visualization.draw(d)
		glRotatef(-self.rot[1], 0, 0, 1)
		glRotatef(-self.rot[1], 0, 1, 0)
		glRotatef(-self.rot[0], 1, 0, 0)
		glTranslatef(*[-x for x in self.pos])

#WIP
#image or image sequence, can be transformed as if it were a model
#has no depth
class Sprite:
	def __init__(self):
		pass

#WIP
#image or image sequence
#always flat against the screen
#does not exist in the 3d space
class Overlay:
	def __init__(self):
		pass
