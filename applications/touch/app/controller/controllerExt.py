"""
The controller class works as the main logic holder for the user triggering scene changes and 
cleaning the canvas / toggling the mic
"""
from datetime import datetime
import settings

class ControllerExt:

	def __init__( self, ownerComp ):
		self.ownerComp = ownerComp
		self.session = op("session") # what session number is this
		self.user_trigger = op("user_trigger") # trigger used to create a new user
		self.count_op = op("count1")
		self.scene_manager_status = op("/app/scene_manager/status_master")

	#### Sessions and user analytics ####

	def NewUser(self):
		"""
		Update the user session
		"""
		self.user_trigger.par.triggerpulse.pulse()
		op.log.Info("Start new user session {0:.0f}".format(self.session["user_id"].eval()))
		op.match.ext.matchExt.Reset()
		op.map.ext.mapExt.ResetMap()

	def StartNewSession(self):
		"""
		Called when the user hits the start button. This function will create a new user and transition
		to the interactive scene
		"""
		op.controller.NewUser()
		op.scene_manager.TransitionToSub('app', 'MAP', 'TUTORIAL')

	def initializeUser(self):
		"""
		Set all of the default values on a new session starting for this user
		"""
		me.store("starttime", datetime.now())
		me.unstore("tree_id")
		me.unstore("connected")

	def FinishSession(self):
		"""
		On a user finishing their session transition back to attract, stop audio, and store the user analytics
		"""
		op.scene_manager.TransitionTo("app", "ATTRACT")
		endtime = datetime.now()
		op.analytics.AddSession(self.session["user_id"].eval(), me.fetch("starttime", endtime), endtime, 
								me.fetch("created_painting", 0), me.fetch("connected", 0), me.fetch("tree_id", ''))


	def Reset(self):
		"""
		Reset the controller. Set the user number to 0 and toggle on the correct app instance
		"""
		op.log.Verbose("Reset the controller")
		self.count_op.par.reset.pulse()
		app_comp = op("/app/scene_app")
		if op.env.Get("APP_INSTANCE") == "app":
			app_comp.allowCooking = True
			# reset the scene manager which will transition to the attract screen
			op.scene_manager.Reset()
			# trigger the blackout
			blackout_trigger = op("blackout_trigger")
			blackout_trigger.par.triggerpulse.pulse()
			

	####### App logic #######
	def SearchArea(self):
		"""
		Search the currently set area
		Returns true if some trees are found, false otherwise
		If there are trees move on to matching
		"""
		# query the server
		if op.data.QueryCurrentArea():
			# there are trees to match with, move on to the matching scene
			op.scene_manager.TransitionToSub('app', 'MATCHING', 'TUTORIAL')
			return True
		else:
			# there are no trees there, raise an error and try again
			pass


	def Match(self, tree_id):
		"""
		tree_id: the id of the tree the user matched with
		"""
		# The user has matched with a tree, we need to play the match animation and then move to the congrats screen
		me.store("tree_id", tree_id)
		op.log.Verbose(f"Made final match with {tree_id}")
		op.data.AddSelectedTree(tree_id)
		op.scene_manager.TransitionToSub('app', 'MATCHING', 'MATCHED')
		# update the matched page
		op.match.ext.matchExt.UpdateMatchedBio()

	def ViewCity(self):
		"""
		After learning more about the tree, see the tree on the map and then see the entire city
		"""

		op.scene_manager.TransitionToSub('app', 'MAP', 'CONNECTED')
