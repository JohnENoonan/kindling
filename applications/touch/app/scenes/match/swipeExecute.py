# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

index_op = op("index")
num_trees_op = op("/app/data/num_trees")

def onOffToOn(channel, sampleIndex, val, prev):
	is_last = index_op['index'].eval() == num_trees_op['num_trees'].eval()
	op.log.Debug(is_last)
	if channel.name == "swipe_up":
		op.match.ext.matchExt.SwipeUp()
	elif channel.name == "swipe_right":
		op.log.Debug(f"swipe right is_last = {is_last}")
		op.match.ext.matchExt.SwipeRight(override=is_last)
	elif is_last:
		# if there are no more trees and they have swiped left 
		op.match.ext.matchExt.HandleNoMatches()

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	