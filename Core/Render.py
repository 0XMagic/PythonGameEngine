import ctypes
from pyglet.gl import *

self = pyglet.window.Window(visible = False)
self.close()

render_queue = dict()


def add(uid, mdl):
	if uid in render_queue:
		return False
	render_queue[uid] = mdl
	return True

def remove(uid):
	if uid in render_queue:
		render_queue.pop(uid)
		return True
	return False


def bind(_self):
	global self
	self = _self
	self.on_resize = _resize
	self.on_draw = _draw
	pass


def _resize(width, height):
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60., float(width) / height, 0.01, 100.)
	glViewport(0, 0, 1280, 720)
	glMatrixMode(GL_MODELVIEW)
	return True


_camera = [
		(0, 0, 0),  #position: x,y,z
		(0, 0, 0),  #rotation matrix
		90  #fov
]


def cam_pos(x, y, z):
	_camera[0] = (x, y, z)


def cam_ang(x, y, z):
	_camera[1] = (x, y, z)


def cam_fov(d):
	_camera[2] = d


def _draw():
	lightfv = ctypes.c_float * 4
	self.clear()
	glLoadIdentity()

	glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-10.0, 200.0, 100.0, 0.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.6, 0.5, 1.0))
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

	glRotatef(_camera[1][0], 1, 0, 0)
	glRotatef(_camera[1][1], 0, 1, 0)
	glTranslatef(*_camera[0])
	for m in self.models:
		m.draw()
