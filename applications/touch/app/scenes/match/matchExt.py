from random import random, randint

SWIPE_UP_TIME = 3

class MatchExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.index_op = op("index")
		self.current_tree_op = op("current_tree")
		self.all_trees = op("trees")
		self.random_op = op("random_match")
		self.matches_table = op("matches")
		self.match_timer_op = op("match_timer")
		self.show_dialogue_op = op("match_dialogue_geo/show_dialogue")
		self.ClearMatches()

	def ClearMatches(self):
		self.matches_table.clear()
		self.matches_table.appendRow(["local_id", "tree_id", "match_time"])

	def addToMatches(self, local_id, tree_id, time_to_match=SWIPE_UP_TIME):
		# add this tree to the match list
		self.matches_table.appendRow([local_id, tree_id, time_to_match + self.match_timer_op["timer_seconds"]])

	def SwipeRight(self):
		# randomly decide if and when a match will happen
		if random() <= op.env.Get("MATCH_PERCENTAGE"):
			time_to_match = randint(int(op.env.Get("MATCH_MIN_DUR")), int(op.env.Get("MATCH_MAX_DUR")))
			op.log.Verbose(f"Matched on right swipe with {self.current_tree_op[1, 'local_id']}, applies in {time_to_match} seconds")
			self.addToMatches(	self.current_tree_op[1, 'local_id'], 
								self.current_tree_op[1, 'tree_id'], 
								time_to_match)

	def ShowMatchDialogue(self, show):
		# set whether to show the matching dialogue
		self.show_dialogue_op.par.value0.val = show
		# pause timer on other matches
		self.match_timer_op.par.play = not show

	def SwipeUp(self):
		# on swipe up we match immediately 
		self.addToMatches(self.current_tree_op[1, 'local_id'], self.current_tree_op[1, 'tree_id'])
		op.log.Verbose("Match on swipe up")

	def HandlePotentialMatch(self, match_id):

		local_id = self.matches_table[match_id, "local_id"]
		op.log.Debug("match_id = {}, local_id = {}".format(match_id, local_id))
		name = self.all_trees[local_id, "name"]
		neighborhood = self.all_trees[local_id, "neighborhood"]
		op("match_dialogue_geo/name").text = f"{name} from {neighborhood} "

		# show confirm dialogue
		self.ShowMatchDialogue(1)

	def ConfirmMatch(self):
		op.log.Verbose("Confirm match")
		self.ShowMatchDialogue(0)


	def DeclineMatch(self):
		op.log.Verbose("Decline match")
		self.ShowMatchDialogue(0)
		pass
