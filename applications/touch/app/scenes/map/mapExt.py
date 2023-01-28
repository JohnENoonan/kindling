
class MapExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.area_slider_op = op("area_slider_geo")
		self.zoom_slider_op = op("zoom_slider_geo")

	def ResetMap(self):
		self.area_slider_op.par.Value = .5
		self.zoom_slider_op.par.Value = 0.0
		op.touch.ResetPan()
