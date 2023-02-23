# me - this DAT.
# 
# dat - the changed DAT
# rows - a list of row indices
# cols - a list of column indices
# cells - the list of cells that have changed content
# prev - the list of previous string contents of the changed cells
# 
# Make sure the corresponding toggle is enabled in the DAT Execute DAT.
# 
# If rows or columns are deleted, sizeChange will be called instead of row/col/cellChange.

#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Signs a URL using a URL signing secret """
import requests

switch_op = op("switch1")
tree_edit_op = op("tree_image_edit")
name_text_op = op("type_profileName")


def onTableChange(dat):
	# force update the name
	name_text_op.cook(force=True)
	# check if an image exists
	has_image = "https://maps.googleapis.com/maps/api/streetview/metadata?location={},{}&key={}".format(dat[1, "latitude"], dat[1, "longitude"], op.env.Get('GOOGLE_KEY'))
	signed_has_image = op.utils.SignUrl(has_image)
	

	response = requests.get(signed_has_image)
	if response.status_code == 200:
		status = response.json()["status"]
		image_ok = status == "OK"
		if image_ok:
			get_image = "https://maps.googleapis.com/maps/api/streetview?size=600x600&location={},{}&key={}".format(dat[1, "latitude"], dat[1, "longitude"], op.env.Get('GOOGLE_KEY'))
			signed_get_image = op.utils.SignUrl(get_image)
			tree_edit_op.par.file = signed_get_image
			switch_op.par.index = 1
		else:
			switch_op.par.index = 0
	else:
		switch_op.par.index = 0

	return

def onRowChange(dat, rows):
	return

def onColChange(dat, cols):
	return

def onCellChange(dat, cells, prev):
	return

def onSizeChange(dat):
	return
	