_uid = 0
_types = dict()


class InvalidType(Exception):
	def __init__(self, attempt):
		self.message = f"{attempt} is not a valid type\n currently registered types are:\n{_types}"
		super().__init__(self.message)


def ulb(f, t, b): return {"upper": f, "lower": t, "bind": b}


def _new(label = None):
	global _uid
	result = hex(_uid)
	_uid += 1
	if label is None:
		label = result
	_types[result] = label
	return result


def get_name(label):
	if label not in _types:
		raise InvalidType(label)
	return _types.get(label)


NULL = _new()

VEC_2D = _new()
VEC_3D = _new()
VEC_2D_DIRECTIONAL = _new()
VEC_3D_DIRECTIONAL = _new()

#min(max(value,lowerbound),upperbound)
BIND_CLAMP = _new()

#((value+lowerbound) % (upperbound + lowerbound)) - lowerbound
BIND_MODULO = _new()

#values = bounds * values / magnitude(values)
#normal binds are always positive and refer to all combos of positive and negative values
BIND_NORMAL = _new()

MODE2D_XY = _new()
MODE2D_YZ = _new()
MODE2D_XZ = _new()

SET_BIND = _new()
