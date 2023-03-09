from random import random, randint

SWIPE_UP_TIME = .33

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
		self.match_bio_table.appendRow(['spc_latin', 'spc_common', 'name', 'bio', 'neighborhood', 'has_guards', 'root_problems', 'has_lights', 'has_shoes'])
		# ops used for caching the images
		self.cache_op = op("profile1/cache1")
		self.cache_select_op = op("match_bio/cacheselect1")
		# popup
		self.no_matches_trigger = op("/app/scene_app/MATCHING/no_matches/no_matches_trigger")

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
		self.cache_op.par.reset.pulse()
		self.cache_select_op.par.index = 0
		me.unstore("match_local_id")

	def addToMatches(self, local_id, swipe_up, time_to_match=SWIPE_UP_TIME):
		# add this tree to the match list
		# schema = local id and the time relative to the match timer that this match should apply
		self.matches_table.appendRow([local_id, swipe_up, time_to_match + self.match_timer_op["timer_seconds"]])

	def cacheTreeImage(self):
		"""
		Store the current index's tree image in the cache op
		"""
		self.cache_op.par.replaceindex = - (self.matches_table.numRows - 1)
		self.cache_op.par.replace.pulse()

	def SwipeRight(self, override=False):
		# randomly decide if and when a match will happen
		if random() <= op.env.Get("MATCH_PERCENTAGE") or override:
			# create random duration of wait time for match back. If there is an override use SWIPE_UP_TIME
			time_to_match = randint(int(op.env.Get("MATCH_MIN_DUR")), int(op.env.Get("MATCH_MAX_DUR"))) if not override else SWIPE_UP_TIME
			op.log.Verbose(f"Matched on right swipe with {self.current_tree_op[1, 'local_id']}, applies in {time_to_match} seconds")
			self.addToMatches(	self.current_tree_op[1, 'local_id'], 
								int(override), 
								time_to_match)
			self.cacheTreeImage()


	def ShowMatchDialogue(self, show):
		"""
		Show or the match accept/reject buttons
		if the dialogue is showing then pause the matching timer
		"""
		# set whether to show the matching dialogue
		self.show_dialogue_op.par.value0.val = show
		# pause timer on other matches
		self.match_timer_op.par.play = not show

	def SwipeUp(self):
		# on swipe up we match immediately 
		self.addToMatches(self.current_tree_op[1, 'local_id'], 1)
		op.log.Verbose("Match on swipe up")
		self.cacheTreeImage()

	def HandlePotentialMatch(self, match_id):
		"""	called when a match has happened
			if the user right swiped they need to confirm the match
			if they swiped up skip and go to next scene
		"""
		local_id = int(self.matches_table[match_id, "local_id"].val)
		# store the prospective matches local id
		me.store("match_local_id", int(local_id))
		op.log.Debug(f"store local_id {local_id}")

		# handle a successful right swipe
		if not int(self.matches_table[match_id, "swipe_up"].val):
			op.log.Debug("Swiped right")
			name = self.all_trees[local_id, "name"]
			neighborhood = self.all_trees[local_id, "neighborhood"]
			op("match_dialogue_geo/name").text = f"{name} from {neighborhood} "
			op("match_dialogue_geo/cacheselect1").par.index = -match_id +1
			# show confirm dialogue if we don't already have a match
			if op("subscene_raw")["SELECTION"]:
				self.ShowMatchDialogue(1)
		# handle swipe up
		else:
			op.log.Debug("swiped up")
			op.controller.Match(local_id)

	def HandleNoMatches(self):
		"""
		If there are no more trees to show we need to either force a match or 
		show the no match message 
		"""
		num_matches = self.matches_table.numRows - 1
		current_time = self.match_timer_op["timer_seconds"].eval()
		if num_matches > 0:
			# try and force a match to happen
			for i in range(1, num_matches):
				match_time = self.matches_table[i, 'match_time']
				# if this match hasn't been processed yet force it by making it a swipe up and happen now
				if match_time > current_time:
					self.matches_table[i, 'match_time'] = -1
					self.matches_table[i, 'swipe_up'] = 1
					return
			# if no matches could be forced we need to start over
			self.ShowNoMatchesPopup()
		else:
			# they have no possible matches, we must show the no matches dialogue and start over
			self.ShowNoMatchesPopup()

	def ShowNoMatchesPopup(self):
		# show the no matches popup and then end this user's session
		dur = 1000 * (self.no_matches_trigger.par.peaklen + self.no_matches_trigger.par.release * 2.0)
		self.no_matches_trigger.par.triggerpulse.pulse()
		run('op.controller.FinishSession()', delayMilliSeconds=dur)
		op.touch.SetActive(0)



	def ConfirmMatch(self):
		"""
		The user has confirmed that the local match is the one for them :) 
		hide dialogue and go to the matched scene
		"""
		op.log.Verbose("Confirm match")
		op.controller.Match(me.fetch("match_local_id"))
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
		cell = -1 * self.matches_table.findCell(str(local_id), cols=['local_id']).row + 1
		self.cache_select_op.par.index = cell
		self.CreateQR(local_id)
		self.match_bio_table.clear(keepFirstRow=True)
		self.match_bio_table.appendRow([	self.all_trees[local_id, "spc_latin"],
											self.all_trees[local_id, "spc_common"],
											self.all_trees[local_id, "name"],
											self.all_trees[local_id, "bio"],
											self.all_trees[local_id, "neighborhood"],
											self.all_trees[local_id, "has_guards"], 
											self.all_trees[local_id, "root_problems"],
											self.all_trees[local_id, "has_lights"],
											self.all_trees[local_id, "has_shoes"]
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

	def SkipTutorial(self):
		# force timer to finish
		op("tutorial/timer1").goToCycleEnd()