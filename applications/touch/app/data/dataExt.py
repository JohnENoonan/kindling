import requests
import json

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

		self.tree_table = op("trees_edit")


	def QueryArea(self, lat, lon, rad):
		params = {
			'latitude': lat,
			'longitude': lon,
			'radius': rad,
		}
		response = requests.get(self.areaUrl, params=params)
		return response.json()

	def processResponse(self, data):
		"""
		Process the API response of querying the area. Data must be a list of dicts
		"""
		# get keys
		keys = list(data[0].keys())
		keys.remove("features")
		keys = ['local_id'] + keys
		features_keys = list(data[0]["features"].keys())
		# set up tables
		self.tree_table.clear()
		self.tree_table.appendRow(keys + features_keys)
		local_id = 1
		for tree in data:
			# main fields
			fields = [local_id] + [tree[key] for key in keys[1:] ]
			# features
			features = [tree["features"][key] for key in features_keys]
			self.tree_table.appendRow(fields + features)
			local_id += 1

	def QueryCurrentArea(self):
		rad = self.raduisOp[0].eval()
		lat = self.pinpointOp[1].eval()
		lon = self.pinpointOp[0].eval()
		response = self.QueryArea(lat, lon, rad)
		if len(response) > 0:
			self.processResponse(response)
		else:
			op.log.Error(f"No trees returned from query to {lat}, {lon} with radius {rad}")

	def GetSelectedTrees(self):
		response = requests.get(self.selectedTreesUrl)

	def AddSelectedTree(self, treeid):
		data = '{{treeid}}'
		response = requests.post(self.selectedTreesUrl, headers=headers, data=data)