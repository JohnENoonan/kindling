from random import random, randint

SWIPE_UP_TIME = 1.5

class MatchExt:

	def __init__(self, ownerComp):
		self.current_tree_op = op("current_tree") # the current tree being examined
		self.all_trees = op("trees") # table of all available trees
		self.matches_table = op("matches") # table storing the matches
		self.match_timer_op = op("match_timer")
		self.show_dialogue_op = op("match_dialogue_geo/show_dialogue")
		# ops used for the matched tree
		self.qr_op = op("match_bio/QRMaker")
		self.match_bio_table = op("match_bio/bio_edit")
		self.match_bio_table.clear()
		self.match_bio_table.appendRow(['spc_latin', 'spc_common', 'name', 'bio', 'neighborhood'])
		self.Reset()

	def ClearMatches(self):
		"""
		Clear all the possible matches
		"""
		self.matches_table.clear()
		self.matches_table.appendRow(["local_id", "swipe_up", "match_time"])

	def Reset(self):
		op.log.Debug("Reset matching")
		self.ClearMatches()
		self.ShowMatchDialogue(0)
		me.unstore("match_local_id")

	def addToMatches(self, local_id, swipe_up, time_to_match=SWIPE_UP_TIME):
		# add this tree to the match list
		# schema = local id and the time relative to the match timer that this match should apply
		self.matches_table.appendRow([local_id, swipe_up, time_to_match + self.match_timer_op["timer_seconds"]])

	def SwipeRight(self):
		# randomly decide if and when a match will happen
		if random() <= op.env.Get("MATCH_PERCENTAGE"):
			time_to_match = randint(int(op.env.Get("MATCH_MIN_DUR")), int(op.env.Get("MATCH_MAX_DUR")))
			op.log.Verbose(f"Matched on right swipe with {self.current_tree_op[1, 'local_id']}, applies in {time_to_match} seconds")
			self.addToMatches(	self.current_tree_op[1, 'local_id'], 
								0, 
								time_to_match)

	def ShowMatchDialogue(self, show):
		"""
		Show or the match accept/reject buttons
		if the dialogue is showing then pause the matching timer
		"""
		op.log.Debug("show show_dialogue = {}".format(show))
		# set whether to show the matching dialogue
		self.show_dialogue_op.par.value0.val = show
		# pause timer on other matches
		self.match_timer_op.par.play = not show

	def SwipeUp(self):
		# on swipe up we match immediately 
		self.addToMatches(self.current_tree_op[1, 'local_id'], 1)
		op.log.Verbose("Match on swipe up")

	def HandlePotentialMatch(self, match_id):
		"""	called when a match has happened
			if the user right swiped they need to confirm the match
			if they swiped up skip and go to next scene
		"""
		local_id = self.matches_table[match_id, "local_id"]
		# store the prospective matches local id
		me.store("match_local_id", int(local_id))

		if not int(self.matches_table[match_id, "swipe_up"].val):
			op.log.Debug("Swiped right")
			name = self.all_trees[local_id, "name"]
			neighborhood = self.all_trees[local_id, "neighborhood"]
			op("match_dialogue_geo/name").text = f"{name} from {neighborhood} "
			# show confirm dialogue
			self.ShowMatchDialogue(1)
		else:
			op.log.Debug("swiped up")
			op.controller.Match(self.all_trees[local_id, "tree_id"])


	def ConfirmMatch(self):
		"""
		The user has confirmed that the local match is the one for them :) 
		hide dialogue and go to the matched scene
		"""
		op.log.Verbose("Confirm match")
		op.controller.Match(self.all_trees[me.fetch("match_local_id"), "tree_id"])
		self.ShowMatchDialogue(0)


	def DeclineMatch(self):
		"""
		The user has chosen to keep looking, hide the dialogue and remove the local match id
		"""
		op.log.Verbose("Decline match")
		self.ShowMatchDialogue(0)
		# unstore the potential local id, this tree isn't it
		me.unstore("match_local_id")

	def UpdateMatchedBio(self):
		local_id = me.fetch("match_local_id")
		self.CreateQR(local_id)
		self.match_bio_table.clear(keepFirstRow=True)
		self.match_bio_table.appendRow([	self.all_trees[local_id, "spc_latin"],
											self.all_trees[local_id, "spc_common"],
											self.all_trees[local_id, "name"],
											self.all_trees[local_id, "bio"],
											self.all_trees[local_id, "neighborhood"]
		])


	def CreateQR(self, local_id):
		"""
		Update the QR code to the url for the matched lat and long. 
		local_id: local id of the tree to update to
		"""
		lat = self.all_trees[local_id, "latitude"]
		lon = self.all_trees[local_id, "longitude"]
		self.qr_op.par.Data = f'http://maps.google.com/maps?q=loc:{lat},{lon}'
		self.qr_op.par.Make.pulse()
