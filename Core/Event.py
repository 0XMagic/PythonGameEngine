import pyglet
from pyglet.window.key import _key_names

self = pyglet.window.Window(visible = False)
self.close()
max_value = 0
keys = {v: k for k, v in _key_names.items()}
_bind_uid = 0


def new_id():
	global _bind_uid
	_bind_uid += 1
	return "#" + hex(_bind_uid)[2:]


class _Mouse:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0

		self.scroll_x = 0
		self.scroll_y = 0
		self.press_x = 0
		self.press_y = 0
		self.rel_x = 0
		self.rel_y = 0

		self.scroll_dx = 0
		self.scroll_dy = 0

		self.holding = None
		self.buttons = dict()
		self.active = {
				"click":  True,
				"pos":    True,
				"scroll": False
		}


def exc(st):
	for _b in self.binds:
		if _b.startswith(st):
			self.binds[_b][0]()


def _scroll(x, y, sx, sy):
	if not self.mouse.active["scroll"]:
		return
	self.mouse.scroll_x = x
	self.mouse.scroll_y = y
	self.mouse.scroll_dx = sx
	self.mouse.scroll_dy = sy
	exc("pr.scroll")


def _release(x, y, b, m):
	if not self.mouse.active["click"]:
		return
	self.mouse.rel_x = x
	self.mouse.rel_y = y
	self.mouse.buttons[b] = False
	exc("rl.mp")
	pass


def _press(x, y, b, m):
	if not self.mouse.active["click"]:
		return
	self.mouse.press_x = x
	self.mouse.press_y = y
	self.mouse.buttons[b] = True
	exc("pr.mp")


def _drag(x, y, dx, dy, b, m):
	if not self.mouse.active["pos"]:
		return
	self.mouse.dx = dx
	self.mouse.dy = dy
	self.mouse.x = x
	self.mouse.y = y

	exc("pr.mv")
	exc("pr.drg")


def _move(x, y, dx, dy):
	if not self.mouse.active["pos"]:
		return
	self.mouse.dx = dx
	self.mouse.dy = dy
	self.mouse.x = x
	self.mouse.y = y
	exc("pr.mv")


def _enter(x, y):
	self.mouse.dx = 0
	self.mouse.dx = 0
	self.mouse.active["pos"] = True
	self.mouse.active["click"] = True
	self.mouse.active["scroll"] = True
	self.set_exclusive_mouse(True)

	pass


def _leave(x, y):
	self.mouse.active["pos"] = False
	self.mouse.active["click"] = False
	self.mouse.active["scroll"] = False
	self.set_exclusive_mouse(False)

	pass


def _key_press(k, m):
	for _b in self.binds:
		if _b.startswith("pr." + str(k)):
			self.binds[_b][0]()
	pass


def _key_release(k, m):
	for _b in self.binds:
		if _b.startswith("rl." + str(k)):
			self.binds[_b][0]()
	pass


def _event_loop(lag):
	for x in self.event_loop_items:
		for y in self.event_loop_items[x]:
			for z in self.event_loop_items[x][y]:
				z()
	pass


def bind(_self):
	global self
	self = _self
	self.mouse = _Mouse()
	self.on_mouse_drag = _drag
	self.on_mouse_enter = _enter
	self.on_mouse_leave = _leave
	self.on_mouse_press = _press
	self.on_mouse_release = _release
	self.on_mouse_scroll = _scroll
	self.on_mouse_motion = _move
	self.update = _event_loop
	self.on_key_press = _key_press
	self.on_key_release = _key_release
	self.event_loop_items = dict()
	self.binds = dict()


"""
----===keybinds===----

bind functions are always in a list, this is to allow for toggle bind functionality 
except for toggle binds, this list will have only 1 item

when a key event is called:
	the exc() function is called with an identifier of to what called it plus key arguments (if applicable)
	
	examples
		pressing key 64 would result in the identifier 'pr.64'
		releasing key 48 would result in the identifier 'rl.48'
		mouse movement is counted as a 'press' and is identified by 'pr.mv'
		
		unlike keyboard information, mouse location/button information is stored in the 
		_Mouse class. 
		(TODO: convert mouse button information to the normal format, mouse button binds are currently impossible!)
	
when the exc() function is called:
	the self.binds dict is evaluated in a for loop
	everything that satisfies '.startswith(identifier)' will have it's 0th executed
	
why they are in lists (toggle keybinds)
		for normal items, the 0th item is the function itself
		for toggle items, the list is 3 items in size instead of 1
		
		if is structured as such
		[meta-function, on function, off function]
		
		note: when a function is called, it has access to it's own bind index and can modify bind functions.
		this is integral for toggle functions to work.
		
		when a toggle bind is called, it's meta-function will be executed, since it is the 0th element
		the meta function then calls the 1st item in it's own list
		then it will pop the 1st item, appending it to itself
		this effectively swaps the position of the on and off functions
		
		this creates a 2-state function that is completely modular to the 1-item-1-function schema
		
		this also allows a bind of n-states to exist since it effectively 'scrolls' through the function list
		(similar to how elements 'scroll' through a list in bubble/shell sort)
"""


def nothing(*args, **kwargs):
	return


def keybind_press(k, func):
	i = new_id()
	k = str(keys.get(k, k))
	self.binds["pr." + k + i] = [func]
	return k + i


def keybind_press_and_release(k, func_on, func_off):
	i = new_id()
	k = str(keys.get(k, k))
	self.binds["pr." + k + i] = [func_on]
	self.binds["rl." + k + i] = [func_off]
	return k + i


def keybind_toggle(k, func_on, func_off):
	i = new_id()
	k = str(keys.get(k, k))

	def result():
		self.binds["pr." + k + i][1]()
		self.binds["pr." + k + i].append(self.binds["pr." + k + i].pop(1))

	self.binds["pr." + k + i] = [result, func_on, func_off]
	return k + i


def add_evl(func, priority):
	#this is not a keybind, this adds items to the event loop
	#items here will run once every game tick
	#use the priority argument
	i = new_id()
	global max_value
	if priority > max_value:
		max_value = priority
	if priority not in self.event_loop_items:
		self.event_loop_items[priority] = dict()
	self.event_loop_items[priority][i] = func
