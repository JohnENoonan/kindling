import requests
import json
import time

headers = {
	'Content-Type': 'application/x-www-form-urlencoded',
}

class DataExt:

	def __init__( self, ownerComp ):
		self.ownerComp = ownerComp
		self.server = op.env.Get("SERVER")
		self.areaUrl = self.server + '/all-trees'
		self.selectedTreesUrl = self.server + '/selected-trees'
		self.raduisOp = op("/app/scene_app/MAP/area_radius")
		self.pinpointOp = op("/app/scene_app/MAP/pin_point")

		self.all_trees_client = op("all_trees_webclient")
		self.selected_trees_client = op("selected_trees_webclient")

		self.tree_table = op("trees_edit")
		self.selected_table = op("selected_edit")

	def convertAPIToTable(self, data, table):
		keys = list(data[0].keys())
		keys.remove("features")
		keys = ['local_id'] + keys
		features_keys = list(data[0]["features"].keys())
		# set up tables
		table.clear()
		table.appendRow(keys + features_keys)
		local_id = 1
		for tree in data:
			# main fields
			fields = [local_id] + [tree[key] for key in keys[1:] ]
			# features
			features = [tree["features"][key] for key in features_keys]
			table.appendRow(fields + features)
			local_id += 1

	def ProcessAllTreesResponse(self, data):
		"""
		Process the API response of querying the area. Data must be a list of dicts
		"""
		# get keys
		self.convertAPIToTable(data, self.tree_table)

	def ProcessSelectedResponse(self, data):
		"""
		Process the API response of all the selected trees. Data must be a list of dicts
		"""
		self.convertAPIToTable(data, self.selected_table)

	def QueryCurrentArea(self):
		rad = self.raduisOp[0].eval()
		lat = self.pinpointOp[1].eval()
		lon = self.pinpointOp[0].eval()
		# start = time.time()
		query = "{}?latitude={}&longitude={}&radius={}".format(self.areaUrl, lat, lon, rad)
		self.all_trees_client.par.url = query
		self.all_trees_client.par.request.pulse()

	def GetSelectedTrees(self):
		self.selected_trees_client.par.request.pulse()

	def AddSelectedTree(self, treeid):
		data = '{{treeid}}'
		response = requests.post(self.selectedTreesUrl, headers=headers, data=data)