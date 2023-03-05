"""
Interface to call the audio app
"""

class ext:

	def __init__(self, ownerComp):

		self.osc = op("oscout1")
		return


	def Play( self, event ):
		self.osc.sendOSC("/audio/play", [event])
		op.log.Debug(f"send {event}")

	def Stop( self, event ):
		self.osc.sendOSC("/audio/stop", [event])

	def Query(self):
		self.osc.sendOSC("/audio/status/query", [1])

	def PlayStart(self):
		self.Play("start_session")

	def PlayButtonClick(self):
		self.Play("button")

	def PlayMatch(self):
		self.Play("match")

	def PlayFinish(self):
		self.Play("end_session")
