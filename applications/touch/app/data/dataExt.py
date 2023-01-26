import requests

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


	def QueryArea(self, lat, lon, rad):
		params = {
			'latitude': lat,
			'longitude': lon,
			'radius': rad,
		}
		response = requests.get(self.areaUrl, params=params)
		return response.json()

	def QueryCurrentArea(self):
		rad = self.raduisOp[0].eval()
		lat = self.pinpointOp[1].eval()
		lon = self.pinpointOp[0].eval()
		return self.QueryArea(lat, lon, rad)

	def GetSelectedTrees(self):
		response = requests.get(self.selectedTreesUrl)

	def AddSelectedTree(self, treeid):
		data = '{{treeid}}'
		response = requests.post(self.selectedTreesUrl, headers=headers, data=data)