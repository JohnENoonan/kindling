
class TouchExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

		self.pan_speed_op = op("speed1")
		self.map_data_op = op("map_data")
		self.touch_op = op("mtouchin1")
		self.SetActive(1)

	def ResetPan(self):
		self.pan_speed_op.par.reset.pulse()

	def ResetPin(self):
		self.map_data_op.par.value2.val = .5
		self.map_data_op.par.value3.val = .5
		
	def SetActive(self, active):
		self.touch_op.par.active = active