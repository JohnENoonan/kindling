class TouchExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

		self.pan_speed_op = op("speed1")
		self.map_data_op = op("map_data")
		self.touch_op = op("mtouchin1")
		self.pin_hold_op = op("/app/scene_app/MAP/pin_point_calc/hold2")
		self.SetActive(1)

	def ResetPan(self):
		# reset the speed chops keeping track of the pan
		op("speed2").par.reset.pulse()
		op("speed3").par.reset.pulse()

	def ResetPin(self):
		self.map_data_op.par.value2.val = .4888
		self.map_data_op.par.value3.val = .6492
		self.pin_hold_op.par.hold.pulse()
		
	def SetActive(self, active):
		self.touch_op.par.active = active