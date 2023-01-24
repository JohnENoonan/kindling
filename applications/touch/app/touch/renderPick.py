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

map_geo = op("/app/scene_app/MAP/map_geo/null1")

area_slider_geo = op("/app/scene_app/MAP/area_slider_geo/slider")
area_slider = op("/app/scene_app/MAP/area_slider_geo")

zoom_slider_geo = op("/app/scene_app/MAP/zoom_slider_geo/slider")
zoom_slider = op("/app/scene_app/MAP/zoom_slider_geo")

map_shader = op("/app/scene_app/MAP/map_shader")
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
			current_uv = (event.u, event.v)
			prev_uv = me.fetch("prev_uv", current_uv)
			if event.selectStart:
				print("start click")
				prev_uv = current_uv
			if event.select:
				delta = tuple(np.subtract(current_uv, prev_uv))
				setDelta(delta)
				setCurrent(current_uv)
				me.store("prev_uv", current_uv)
			if event.selectEnd:
				print("select end")
				setDelta((0.0, 0.0))
		# drag area slider
		elif event.selectedOp == area_slider_geo and event.select:
			area_slider.par.Value = event.texture[0];
		# drag zoom slider
		elif event.selectedOp == zoom_slider_geo and event.select:
			zoom_slider.par.Value = event.texture[0];


	return

	