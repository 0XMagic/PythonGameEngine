import math


class Angle:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0
		self.vn = VectorNormed()

	def __call__(self, *args, **kwargs):
		#gets x,y,z as radians
		if len(args) != 0:
			return tuple([math.radians(w) for w in [self.x, self.y, self.z]])
		return self.x, self.y, self.z

	def __getitem__(self, item, *args):
		return self(*args)[item]

	def vector(self):
		rx, ry, rz = self("r")
		self.vn.x, self.vn.y, self.vn.z = math.cos(rx) * math.sin(ry), math.sin(rx), math.cos(rx) * math.cos(ry)
		return self.vn


class Vector:
	def __init__(self, *args):
		self.x = 0
		self.y = 0
		self.z = 0
		if len(args) != 0:
			self.x = args[0][0]
			self.y = args[0][1]
			self.z = args[0][2]

	def reset(self):
		self.x *= 0
		self.y *= 0
		self.z *= 0

	def add_vec(self, n_vec):
		self.x += n_vec[0]
		self.y += n_vec[1]
		self.z += n_vec[2]

	def set(self, vec):
		self.x = vec[0]
		self.y = vec[1]
		self.z = vec[2]

	def norm(self):
		result = VectorNormed()
		result.x = self.x
		result.y = self.y
		result.z = self.z
		result.norm()
		return result

	def __call__(self, *args, **kwargs):
		return self.x, self.y, self.z

	def __getitem__(self, item):
		return self()[item]

	def __abs__(self):
		return Vector([abs(self[x]) for x in range(3)])

	def __add__(self, other):
		return Vector([other[x] + self[x] for x in range(3)])

	def __radd__(self, other):
		return Vector([self[x] + other[x] for x in range(3)])

	def __sub__(self, other):
		return Vector([self[x] - other[x] for x in range(3)])

	def __rsub__(self, other):
		return Vector([other[x] - self[x] for x in range(3)])

	def __mul__(self, other):
		return Vector([other[x] * self[x] for x in range(3)])

	def __rmul__(self, other):
		return Vector([self[x] * other[x] for x in range(3)])

	def __truediv__(self, other):
		return Vector([self[x] / other[x] for x in range(3)])

	def __rtruediv__(self, other):
		return Vector([other[x] / self[x] for x in range(3)])

	def __ge__(self, other):
		return Vector([other[x] < self[x] for x in range(3)])

	def __le__(self, other):
		return Vector([other[x] > self[x] for x in range(3)])

	def __eq__(self, other):
		return Vector([other[x] == self[x] for x in range(3)])

	def __repr__(self):
		return "Vector[x={},y={},z={}]".format(self.x, self.y, self.z)


class VectorNormed:
	def __init__(self, *args):
		self.x = 0
		self.y = 0
		self.z = 0
		if len(args) != 0:
			self.x = args[0][0]
			self.y = args[0][1]
			self.z = args[0][2]

	def norm(self):
		m = sum([w ** 2 for w in [self.x, self.y, self.z]])
		if m != 0:
			m = m ** (-0.5)
		else:
			m = 0
		self.x, self.y, self.z = tuple([m * w for w in [self.x, self.y, self.z]])
		return self

	def denorm(self):
		result = Vector()
		result.x = self.x
		result.y = self.y
		result.z = self.z
		return result

	def __call__(self, *args, **kwargs):
		return self.x, self.y, self.z

	def __getitem__(self, item):
		return self()[item]

	def __abs__(self):
		return VectorNormed([abs(self[x]) for x in range(3)])

	def __add__(self, other):
		return VectorNormed([other[x] + self[x] for x in range(3)])

	def __radd__(self, other):
		return VectorNormed([self[x] + other[x] for x in range(3)])

	def __sub__(self, other):
		return VectorNormed([self[x] - other[x] for x in range(3)])

	def __rsub__(self, other):
		return VectorNormed([other[x] - self[x] for x in range(3)])

	def __mul__(self, other):
		return VectorNormed([other[x] * self[x] for x in range(3)])

	def __rmul__(self, other):
		return VectorNormed([self[x] * other[x] for x in range(3)])

	def __truediv__(self, other):
		return VectorNormed([self[x] / other[x] for x in range(3)])

	def __rtruediv__(self, other):
		return VectorNormed([other[x] / self[x] for x in range(3)])

	def __ge__(self, other):
		return Vector([other[x] < self[x] for x in range(3)])

	def __le__(self, other):
		return Vector([other[x] > self[x] for x in range(3)])

	def __eq__(self, other):
		return Vector([other[x] == self[x] for x in range(3)])

	def __repr__(self):
		return "VectorNormed[x={},y={},z={}]".format(self.x, self.y, self.z)

	def add_vec(self, n_vec):
		self.norm()
		self.x += n_vec[0]
		self.y += n_vec[1]
		self.z += n_vec[2]
		self.norm()

	def set(self, vec):
		self.x = vec[0]
		self.y = vec[1]
		self.z = vec[2]
		self.norm()
