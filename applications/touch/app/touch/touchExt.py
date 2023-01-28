

class TouchExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

		self. pan_speed_op = op("speed1")

	def ResetPan(self):
		self.pan_speed_op.par.reset.pulse()