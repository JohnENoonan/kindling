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

		self.all_trees_client = op("all_trees_webclient")
		self.selected_trees_client = op("selected_trees_webclient")
		self.post_tree_client = op("post_tree_webclient")

		self.tree_table = op("trees_edit")
		self.selected_table = op("selected_edit")
		self.selected_lat_lon_op = op("selected_lat_lon")


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
		# self.convertAPIToTable(data, self.selected_table)
		keys = ['tree_id', 'species_id', 'latitude', 'longitude']
		features_keys = ['diameter', 'introverted', 'has_guards', 'root_problems', 'has_lights', 'has_shoes', 'zipcode']
		self.selected_table.clear()
		self.selected_table.appendRow(keys + features_keys)
		for tree in data:
			# main fields
			fields = [tree[key] for key in keys ]
			# features
			features = [tree["features"][key] for key in features_keys]
			self.selected_table.appendRow(fields + features)

	def QueryCurrentArea(self):
		rad = self.raduisOp[0].eval()
		lat = self.pinpointOp[1].eval()
		lon = self.pinpointOp[0].eval()
		query = "{}?latitude={}&longitude={}&radius={}".format(self.areaUrl, lat, lon, rad)
		self.all_trees_client.par.url = query
		self.all_trees_client.par.request.pulse()

	def GetSelectedTrees(self):
		self.selected_trees_client.par.request.pulse()


	def assemblJson(self, i):

		#local_id	tree_id	species_id	spc_latin	spc_common	name	latitude	longitude	bio	selected	diameter	introverted	has_guards	root_problems	has_lights	has_shoes	address	zipcode	neighborhood
		return {
			'tree_id': int(self.tree_table[i, 'tree_id'].val),
			'species_id': int(self.tree_table[i, 'species_id'].val),
			'spc_latin': self.tree_table[i, 'spc_latin'].val,
			'spc_common': self.tree_table[i, 'spc_common'].val,
			'name': self.tree_table[i, 'name'].val,
			'latitude': float(self.tree_table[i, 'latitude'].val),
			'longitude': float(self.tree_table[i, 'longitude'].val),
			'bio': self.tree_table[i, 'bio'].val,
			'selected': bool(self.tree_table[i, 'selected'].val),
			"features": {
				'diameter': int(self.tree_table[i, 'diameter'].val),
				'introverted': bool(self.tree_table[i, 'introverted'].val),
				'has_guards': bool(self.tree_table[i, 'has_guards'].val),
				'root_problems': bool(self.tree_table[i, 'root_problems'].val),
				'has_lights': bool(self.tree_table[i, 'has_lights'].val),
				'has_shoes': bool(self.tree_table[i, 'has_shoes'].val),
				'address': self.tree_table[i, 'address'].val,
				'zipcode': int(self.tree_table[i, 'zipcode'].val),
				'neighborhood': self.tree_table[i, 'neighborhood'].val,
			}
		}

	def AddSelectedTree(self, local_id):
		"""
		Add a tree as having been selected
		local_id: the local_id of the tree to add
		"""
		obj = self.assemblJson(local_id)
		# store the selected lat lon
		self.selected_lat_lon_op.par.value0.val = obj['latitude']
		self.selected_lat_lon_op.par.value1.val = obj['longitude']
		self.post_tree_client.request(self.selectedTreesUrl, "POST", header={'Content-type': 'application/json', 'Accept': 'text/plain'}, data=json.dumps(obj))

	def GetTreeIdFromLocal(self, local_id):
		"""
		Convert a local id to the tree id
		Return int(tree_id) or '' if the local_id is None
		"""
		if local_id is not None:
			return self.tree_table[local_id, 'tree_id'].val
		return ''


	def GetLocalName(self, local_id):
		return self.tree_table[local_id, 'name'].val