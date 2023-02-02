"""
This class serves as a helper for writing out the analytics for a user session
"""
import os
from datetime import datetime

class AnalyticsExt:

	header = "uid,starttime,endtime,duration,connected,treeid"

	def __init__( self, ownerComp ):
		self.folder = str(parent().par.Analyticsfolder)
		self.filename = "analytics.csv"
		self.outfilepath = os.path.join(self.folder, self.filename)

		if not os.path.exists(self.folder):
			op.log.Debug("Created analytics folder '{}'".format(self.folder))
			os.makedirs(self.folder)

	def datetimeToStr(self, timeobj):
		return timeobj.strftime( "%y/%m/%d %H:%M:%S" )

	def AddSession(self, uid, startitme, endtime, connected, treeid=-1):
		"""
		Append this user session to the analytics file
		"""
		try:
			with open(self.outfilepath, 'a+', encoding='utf-8') as outfile:
				dur = (endtime - startitme).total_seconds()
				session = f"{int(uid)},{self.datetimeToStr(startitme)},{self.datetimeToStr(endtime)},{dur},{connected},{treeid}\n"
				outfile.write(session)		
		except FileNotFoundError:
			op.log.Error("anayltics file '{}'".format(self.outfilepath))
			self.Reset()

	def Reset(self):
		with open(self.outfilepath, 'w', encoding='utf-8') as outfile:
			outfile.write(AnalyticsExt.header + "\n")