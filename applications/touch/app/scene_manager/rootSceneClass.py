"""
	
	Scene Master Class

	Scene instances use these parent callbacks for tween outs and ins

"""

class ext:

	def __init__( self, ownerComp ):

		self.tween_in_node = None
		self.ownerComp = ownerComp
		self.app_id = op('..').name.replace('scene_','')

		if ( not self.ownerComp.name == 'scene_leds' ):
			op('scene_stitch_hold').par.holdpulse.pulse()
			op('subscene_stitch_hold').par.holdpulse.pulse()

		return


	def TweenInResolve( self, which ):
		return


	def PrepTweenIn( self, which ):
		self.tween_in_node = op( which )
		return


	def TweenOutResolve( self, which ):

		if ( not self.ownerComp.name == 'scene_leds' ):
			op('scene_stitch_hold').par.holdpulse.pulse()
			op('subscene_stitch_hold').par.holdpulse.pulse()

		self.tween_in_node.TweenIn()
		
		return


	def SubsceneTweenOutResolve( self ):

		if ( not self.ownerComp.name == 'scene_leds' and not self.ownerComp.name == 'scene_conf' ):
			op('subscene_stitch_hold').par.holdpulse.pulse()

		return


	def TweenOutComplete( self, which ):
		return


	def AppId( self ):
		return self.app_id
