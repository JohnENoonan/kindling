"""

	Utils 
	
	Stateless, misc helper functions, consolidated


"""

import uuid
import os
import re
import time
from datetime import datetime



class ext:

	def __init__( self, ownerComp ):
		return

	def DatRowToArray( self, data ):
		return list( map( lambda x : str( x ), data ) )

	def EnsureDir( self, filepath ):
		is_file = not os.path.splitext( filepath )[1] == ''
		is_dir = os.path.isdir( filepath )
		if not is_file:
			if not is_dir:
				os.makedirs( filepath )
		return

	def NaturalSort( self, l ):
		convert = lambda text: int(text) if text.isdigit() else text.lower() 
		alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
		return sorted(l, key=alphanum_key)

	def UUID( self ):
		return str( uuid.uuid1() )

	def GetTimestamp(self):
		return time.strftime( "%y-%m-%d-%H-%M-%S", time.localtime() )

	def TimeToTimestamp(self, timeobj):
		return timeobj.strftime( "%y-%m-%d-%H-%M-%S" )

	def GetEpochTime(self):
		return int(time.time())