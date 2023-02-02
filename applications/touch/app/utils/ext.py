"""
	Util helper functions
"""

import uuid
import os
import re
import time
from datetime import datetime
import hashlib
import hmac
import base64
import urllib.parse as urlparse



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

	def SignUrl(self, input_url):
		""" Sign a request URL with a URL signing secret.
			Usage:
			from urlsigner import sign_url
			signed_url = sign_url(input_url=my_url, secret=SECRET)
			Args:
			input_url - The URL to sign
			secret    - Your URL signing secret
			Returns:
			The signed request URL
  		"""

		url = urlparse.urlparse(input_url)

		# We only need to sign the path+query part of the string
		url_to_sign = url.path + "?" + url.query

		# Decode the private key into its binary format
		# We need to decode the URL-encoded private key
		decoded_key = base64.urlsafe_b64decode(str(op.env.Get("GOOGLE_SECRET")))

		# Create a signature using the private key and the URL-encoded
		# string using HMAC SHA1. This signature will be binary.
		signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

		# Encode the binary signature into base64 for use within a URL
		encoded_signature = base64.urlsafe_b64encode(signature.digest())

		original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

		# Return signed URL
		return original_url + "&signature=" + encoded_signature.decode()
