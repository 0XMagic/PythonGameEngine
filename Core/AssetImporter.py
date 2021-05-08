import os
import json
from CustomExceptions import *

import pywavefront
import pywavefront.material


def _extract_obj(file):
	result = pywavefront.Wavefront(file)

	return result

_extract = {
		"obj": _extract_obj
}
_queue = dict()
with open("Assets/AssetManager.json") as asm:
	js = json.load(asm)
	print("validating content files...")
	for fl in js:
		if not os.path.isdir("Assets/" + js[fl]):
			raise AssetPathNotFound("Assets/" + js[fl])
		_queue[fl] = ["Assets/" + js[fl] + "/" + _s for _s in os.listdir("Assets/" + js[fl])]


def extract():
	print("extracting content files...")
	result = list()
	for i in _queue:
		sub_result = list()
		for j in _queue[i]:
			k = _extract.get(j.split(".")[-1], None)
			print(i)
			if k is not None:
				k = k(j)
				if k is not None:
					sub_result.append(k)
		result.append(sub_result)
	return result
