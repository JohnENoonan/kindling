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

	def StartNewSession(self):
		"""
		Called when the user hits the start button. This function will create a new user and transition
		to the interactive scene
		"""
		op.controller.NewUser()
		op.scene_manager.TransitionToSub('app', 'MAP', 'AREA')

	def initializeUser(self):
		"""
		Set all of the default values on a new session starting for this user
		"""
		me.store("starttime", datetime.now())

	def FinishSession(self):
		"""
		On a user finishing their session transition back to attract, stop audio, and store the user analytics
		"""
		op.scene_manager.TransitionTo("app", "ATTRACT")
		endtime = datetime.now()
		# op.analytics.AddSession(self.session["user_id"].eval(), me.fetch("starttime", endtime), endtime, 
		# 						me.fetch("created_painting", 0), me.fetch("viewed_gallery", 0), me.fetch("render_name", ''))

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
			
