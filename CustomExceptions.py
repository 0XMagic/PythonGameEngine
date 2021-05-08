class AssetPathNotFound(Exception):
	def __init__(self, fault):
		self.fault = fault

	def __str__(self):
		return "Error whilst using AssetManager:\n[{} does not exist]".format(self.fault)


class AssetMissing(Exception):
	def __init__(self, fault):
		self.fault = fault

	def __str__(self):
		return "Error whilst using loading assets:\n[{} does not exist]".format(self.fault)


class ConvertErrorNumerical(Exception):
	def __init__(self, fault):
		self.fault = fault

	def __str__(self):
		return "Conversion Error:\n{}".format(self.fault)


class ConvertError(Exception):
	def __init__(self,error_type, fault, possible):
		self.err = error_type
		self.possible = possible
		self.fault = fault

	def __str__(self):
		return "{}:\n{} is not a valid choice{}\n".format(self.err,self.fault,self.possible)
