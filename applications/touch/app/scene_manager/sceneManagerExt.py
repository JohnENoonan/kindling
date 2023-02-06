"""
This class handles all the logic for changing scenes. It works with the sceneClass
"""

import json

class ext:

	def __init__( self, ownerComp ):
	
		self.Scenes = {
			'app': ['ATTRACT', 'MAP', 'MATCHING']
		}

		self.scene_ops_list = [ '/app/scene_app/' + scene for scene in self.Scenes["app"] ]

		self.Subscenes = {

			'app': {
				'MAP': [ 'TUTORIAL', 'AREA', 'CONNECTED' ],
				'MATCHING': ['TUTORIAL', 'SELECTION', 'MATCHED']
			}
		}
		

		self.nodes = {
			'app': {
				'scenes': op('scenes_app'),
				'subscenes': op('subscenes_app')
			}
		}

		self.chops = {
			'app': {
				'scenes': {
					'ATTRACT': self.nodes['app']['scenes'].par.value0,
					'MAP': self.nodes['app']['scenes'].par.value1,
					'MATCHING': self.nodes['app']['scenes'].par.value2
				},
				'subscenes': {
					'MAP': {
						'TUTORIAL': self.nodes['app']['subscenes'].par.value0,
						'AREA': self.nodes['app']['subscenes'].par.value1,
						'CONNECTED': self.nodes['app']['subscenes'].par.value2
					},
					'MATCHING': {
						'TUTORIAL': self.nodes['app']['subscenes'].par.value3,
						'SELECTION': self.nodes['app']['subscenes'].par.value4,
						'MATCHED': self.nodes['app']['subscenes'].par.value5
					}
				}
			}
		}

		return


	def Reset( self ):

		for n in self.scene_ops_list:
			o = op( n )
			if ( hasattr( o, 'Reset' ) ):
				op( n ).Reset()
				# op( n ).cook(force=True, recurse=True)
				op.log.Debug( 'Reset ' + o.path )


		run( "op.scene_manager.FinishReset()", delayFrames=300 )


		return


	def FinishReset( self ):
		"""
		Transition through start scenes to make sure all fields are set to the correct defualt
		"""
		delay_len = 120
		self.TransitionTo('app', 'ATTRACT')
		for i, scene in enumerate(["ATTRACT"]):
			run( "op('/app/scene_app/{}').TweenIn()".format(scene), delayFrames=delay_len * i )



	def Clear( self ):
		for app in self.chops:
			for s in self.chops[ app ]['scenes']:
				self.chops[ app ]['scenes'][ s ].val = 0
			for s in self.chops[ app ]['subscenes']:
				for ss in self.chops[ app ]['subscenes'][ s ]:
					self.chops[ app ]['subscenes'][ s ][ ss ].val = 0

	def SetScene( self, app_id, scene, on_off ):
		self.chops[ app_id ]['scenes'][ scene ].val = on_off
		data = {"scene": scene}

	def SetSubscene( self, app_id, scene, subscene, on_off ):
		if ( not subscene == 'DEFAULT' ):
			self.chops[ app_id ]['subscenes'][ scene ][ subscene ].val = on_off

	def TransitionTo( self, app_id, scene):
		"""
		Transition to a scene
		app_id = name of app the scene belongs to
		scene = name of scene to transition to
		"""
		for curr_scene in self.chops[app_id]["scenes"].keys():
			self.SetScene(app_id, curr_scene, 0)
		self.SetScene(app_id, scene, 1)
		op.log.Debug(f"Transition to {app_id}:{scene}")

	def TransitionToSub( self, app_id, scene, subscene):
		"""
		Transition to a subscene
		app_id = name of app the scene belongs to
		scene = name of scene to transition to
		subscene = name of subscene belonging to the scene to transition to
		"""
		for curr_scene in self.chops[app_id]["scenes"].keys():
			self.SetScene(app_id, curr_scene, 0)
		
		for curr_subscene in self.Subscenes[app_id][scene]:
			self.SetSubscene(app_id, scene, curr_subscene, 0)
		self.SetScene(app_id, scene, 1)
		self.SetSubscene(app_id, scene, subscene, 1)
		op.log.Debug(f"Transition to {app_id}:{scene}:{subscene}")

	def GetCurrentScene(self):
		"""
		Return the name of the scene currently running
		"""
		for scene in self.Scenes["app"]:
			if self.nodes["app"]["scenes"][scene] == 1:
				return scene