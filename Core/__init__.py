import Core.Render, Core.Event, Core.AssetImporter, Core.Graphics


def bind(self):
	models = Core.AssetImporter.extract()
	self.models = list()
	for m in models:
		self.models.append(Core.Graphics.Model(m))
	Core.Render.bind(self)
	Core.Event.bind(self)
