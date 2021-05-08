import CustomExceptions
from Instance.ID import *
"""
a potential replacement for Game/Object.py
generalises different vector types 

"""
default_kw = ulb(None, None, None)


class InstVector:
	def __init__(self):
		self.type = NULL
		self.value = [0, 0, 0]
		self.lock = [False, False, False]
		self.bind = [-1, -1, -1]
		self.bounds = [[0, 0], [0, 0], [0, 0]]
		self.mode2d = 0

	#assign will change the type without converting the values,
	#position vector of 1,1,1 can become a directional vector of 1,1,1 for example
	#for this ignores normal limits, note that the directional vector has a magnitude greater than 1
	#this is only corrected the next time the value is evaluated
	def assign(self, t):
		self.type = t
		return self

	def check(self, *t):
		return self.type in t

	#assign will change the type without converting the values,
	#position vector of 1,1,1 can become a directional vector of sqrt(3)/3,sqrt(3)/3,sqrt(3)/3 for example
	def convert(self, con, *args, **kwargs):
		if con == VEC_3D:
			self.lock = (False, False, False)
			if self.check(
					VEC_2D,
					VEC_3D,
					VEC_2D_DIRECTIONAL,
					VEC_3D_DIRECTIONAL
			):
				return self

		if con == SET_BIND:
			x, y, z = [kwargs.get(w, default_kw) for w in ["x", "y", "z"]]
			upper, lower, bind = [[w.get(v, None) for w in [x, y, z]] for v in default_kw.keys()]
			for w in range(3):
				vu, vl, vb = [v[w] for v in [upper, lower, bind]]
				if vu is not None:
					self.bounds[w][0] = vu
				if vl is not None:
					self.bounds[w][1] = vl
				is_valid = min(self.bounds[w]) != max(self.bounds[w])
				if not is_valid:
					CustomExceptions.ConvertErrorNumerical("value maximum is less than or equal to value minimum")
				self.bind[w] = bind[w]
			return self

		if con == VEC_2D:
			if MODE2D_XY in args:
				self.mode2d = MODE2D_XY
				self.lock = (False, False, True)
				self.assign(VEC_2D)
				return self
			if MODE2D_XZ in args:
				self.mode2d = MODE2D_XZ
				self.lock = (False, True, False)
				self.assign(VEC_2D)
				return self
			if MODE2D_YZ in args:
				self.mode2d = MODE2D_YZ
				self.lock = (True, False, False)
				self.assign(VEC_2D)
				return self

