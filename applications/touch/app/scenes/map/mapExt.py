
class MapExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.area_slider_op = op("area_slider_geo")
		self.zoom_slider_op = op("zoom_slider_geo")
		self.tutorial_timer_op = op("tutorial/timer1")

		self.no_trees_trigger_op = op("search_anims/no_trees_trigger")
		self.loading_trigger_op = op("search_anims/loading_trigger")

	def SkipTutorial(self):
		self.tutorial_timer_op.goToCycleEnd()

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
		self.loading_trigger_op.par.triggerpulse.pulse()
		op.touch.SetActive(0)

	def NoTreesAvailable(self):
		"""
		There are no trees in the query just submitted, tell the user and let them try again
		"""
		self.loading_trigger_op.par.triggerpulse.pulse()
		self.no_trees_trigger_op.par.triggerpulse.pulse()
		delay = self.no_trees_trigger_op.par.attack * 2 + self.no_trees_trigger_op.par.peaklen * 1000.0
		run("op.touch.SetActive(1)", delayMilliSeconds=delay)

	def FoundTrees(self):
		"""
		The user's search found trees, we are going to go into the matching process
		"""
		self.loading_trigger_op.par.triggerpulse.pulse()
		op.touch.SetActive(1)