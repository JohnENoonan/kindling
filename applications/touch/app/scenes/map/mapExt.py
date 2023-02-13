
class MapExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.area_slider_op = op("area_slider_geo")
		self.zoom_slider_op = op("zoom_slider_geo")

		self.no_trees_trigger_op = op("search_anims/no_trees_trigger")

	def ResetMap(self):
		op.log.Verbose("Reset Map")
		self.area_slider_op.par.Value = .5
		self.zoom_slider_op.par.Value = 0.0
		op.touch.ResetPan()
		op.touch.ResetPin()

	def StartSearchAnimation(self):
		"""
		The user clicked the search and we need to play the searching animation
		"""
		pass

	def NoTreesAvailable(self):
		"""
		There are no trees in the query just submitted, tell the user and let them try again
		"""
		self.no_trees_trigger_op.par.triggerpulse.pulse()

	def FoundTrees(self):
		"""
		The user's search found trees, we are going to go into the matching process
		"""
		pass