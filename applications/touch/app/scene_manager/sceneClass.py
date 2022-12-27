"""
	
	Scene Instance Class

	Interact with timer chops for tween in and out animation timelines
	Report state back to scene root node


"""

class ext:

	def __init__(self, ownerComp):
		
		self.timer_in = op('animate_in')
		self.timer_out = op('animate_out')
		self.name = op('..').name
		self.app_id = op('../..').name.replace('scene_','')
		self.status = op('status_dat')
		self.status_chop = op('status_chop')
		self.reset = op('reset_subscene_trigger')

		self.VISIBLE = self.status_chop.par.value0
		self.TWEENIN = self.status_chop.par.value1
		self.TWEENOUT = self.status_chop.par.value2
		self.INTERACTIVE = self.status_chop.par.value3

		self.slave = False# ( self.app_id == 'leds' )

		return

	def TweenOut( self ):
		self.TWEENOUT.val = 1
		self.INTERACTIVE.val = 0
		return

	def TweenOutComplete( self ):
		self.TWEENOUT.val = 0
		self.VISIBLE.val = 0
		self.TWEENIN.val = 0
		op('../..').TweenOutComplete( self.name )
		return

	def TweenOutResolve( self ):
		op('../..').TweenOutResolve( self.name )
		return

	def TweenIn( self ):
		self.INTERACTIVE.val = 0
		self.VISIBLE.val = 1
		self.TWEENIN.val = 1
		return

	def TweenInResolve( self ):
		self.INTERACTIVE.val = 1
		self.TWEENIN.val = 0
		op('../..').TweenInResolve( self.name )
		return

	def SubsceenTweenInResolve( self ):
		return

	def SubsceneTweenOutResolve( self ):
		op('../..').SubsceneTweenOutResolve()
		return

	def SubsceenTweenOut( self ):
		return

	def AppId( self ):
		return self.app_id

	def Reset( self ):

		self.INTERACTIVE.val = 0
		self.VISIBLE.val = 1
		self.TWEENIN.val = 0
		self.TWEENOUT.val = 0

		self.timer_out.par.initialize.pulse()
		self.timer_in.par.initialize.pulse()
		self.timer_in.par.start.pulse()

		path = str( op('..') )
		op('..').cook( force=True )
		run( "op('{}').op('animate_in').par.initialize.pulse()".format( path ), delayFrames=( 50 ) )

		self.reset.par.triggerpulse.pulse()

		run( "op('{}').op('status_chop').par.value0.val = 0".format( path ), delayFrames=61 )

		run( "op('{}').cook( force=True )".format( path ), delayFrames=61 )

		return