# The function below is called when any passed values have changed.
# Be sure to turn on the related parameter in the DAT to retrieve these values.
#
# me - this DAT
# renderPickDat - the connected Render Pick DAT
#
# events - a list of named tuples with the fields listed below.
# eventsPrev - a list of events holding the eventsPrev values.
#
#	u				- The selection u coordinate.			(float)
#	v				- The selection v coordinate.			(float)
#	select			- True when a selection is ongoing.		(bool)
#	selectStart		- True at the start of a selection.		(bool)
#	selectEnd		- True at the end of a selection.		(bool)
#	selectedOp		- First picked operator.				(OP)
#	selectedTexture	- Texture coordinate of selectedOp.		(Position)
#	pickOp			- Currently picked operator.			(OP)
#	pos				- 3D position of picked point.			(Position)
#	texture			- Texture coordinate of picked point.	(Position)
#	color			- Color of picked point.				(4-tuple)
#	normal			- Geometry normal of picked point.		(Vector)
#	depth			- Post projection space depth.			(float)
#	instanceId		- Instance ID of the object.			(int)
#	row				- The row associated with this event	(float)
#	inValues		- Dictionary of input DAT strings for the given row, where keys are column headers. (dict)
#	custom	 		- Dictionary of selected custom attributes
import numpy as np



area_slider_geo = op("/app/scene_app/MAP/area_slider_geo/slider")
area_slider = op("/app/scene_app/MAP/area_slider_geo")

zoom_slider_geo = op("/app/scene_app/MAP/zoom_slider_geo/slider")
zoom_slider = op("/app/scene_app/MAP/zoom_slider_geo")

match_confirm_geo = op("/app/scene_app/MATCHING/match_dialogue_geo/match_geo/null1")
match_decline_geo = op("/app/scene_app/MATCHING/match_dialogue_geo/pass_geo/null1")
match_skip = op("/app/scene_app/MATCHING/tutorial/skip_geo/null1")
match_next_geo = op("/app/scene_app/MATCHING/match_bio/next_geo/null1")
match_show_dialogue = op("/app/scene_app/MATCHING/match_dialogue_geo/show_dialogue")

map_submit_geo = op("/app/scene_app/MAP/submit_geo/null1")
map_geo = op("/app/scene_app/MAP/map_geo/null1")
map_shader = op("/app/scene_app/MAP/map_shader")
map_skip = op("/app/scene_app/MAP/tutorial/skip_geo/null1")

# map data is a constant used to write out
map_data = op("map_data")

def setDelta(delta):
	map_data.par.value0.val = delta[0]
	map_data.par.value1.val = delta[1]

def setCurrent(current):
	map_data.par.value2.val = current[0]
	map_data.par.value3.val = current[1]

def onEvents(renderPickDat, events, eventsPrev):

	for event, eventPrev in zip(events, eventsPrev):

		
		# drag map
		if event.selectedOp == map_geo:
			current_uv = event.texture
			prev_uv = me.fetch("prev_uv", current_uv)
			if event.selectStart:
				prev_uv = current_uv
			if event.select:
				delta = tuple(np.subtract(current_uv, prev_uv))
				setDelta(delta)
				setCurrent(current_uv)
				me.store("prev_uv", current_uv)
			if event.selectEnd or event.pickOp != map_geo:
				setDelta((0.0, 0.0))
		elif op.scene_manager.IsMapArea():
			# drag area slider
			if event.selectedOp == area_slider_geo and event.pickOp == area_slider_geo and event.select:
				area_slider.par.Value = event.texture[0]
			# drag zoom slider
			elif event.selectedOp == zoom_slider_geo and event.pickOp == zoom_slider_geo and event.select:
				zoom_slider.par.Value = event.texture[0]
			# submit map
			elif event.selectedOp == map_submit_geo and event.selectEnd:
				op.controller.SearchArea()
		# skip map tutorial
		elif op.scene_manager.IsMapTutorial() and event.selectedOp == map_skip and event.selectEnd:
			op.map.ext.mapExt.SkipTutorial()
		# skip matching tutorial
		elif op.scene_manager.IsMatchingTutorial() and event.selectedOp == match_skip and event.selectEnd:
			op.match.ext.matchExt.SkipTutorial()

		# matching buttons
		if op.scene_manager.IsMatchingSelection() and match_show_dialogue[0][0]:
			if event.selectedOp == match_confirm_geo and event.selectEnd:
				op.match.ext.matchExt.ConfirmMatch()
			elif event.selectedOp == match_decline_geo and event.selectEnd:
				op.match.ext.matchExt.DeclineMatch()
				
		# finish looking at bio
		elif event.selectedOp == match_next_geo and event.selectEnd and op.scene_manager.IsMatchingMatched():
			op.controller.ViewCity()
