#**********************************************************************
#*                      Sploit Mutation Engine                        *
#**********************************************************************
#* Copyright (C) 2004-2007 Davide Balzarotti                          *
#*                                                                    *
#* This program is free software; you can redistribute it and/or      *
#* modify it under the terms of the GNU General Public License        *
#* version 2.                                                         *
#*                                                                    *
#* This program is distributed in the hope that it will be useful,    *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of     *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.               *
#* See the GNU General Public License for more details.               *
#*                                                                    *
#* You should have received a copy of the GNU General Public License  *
#* along with this program; if not, write to the Free Software        *
#* Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.          *
#*********************************************************************/

# Author: Davide Balzarotti
# $Id: snort_collector.py 109 2006-02-27 20:17:42Z balzarot $

import os.path, string

from interfaces.collector import Collector
from interfaces.hasparameters import StringParam

class LSnortCollector(Collector):
	'''Local Snort Collector '''
	
	def __init__(self):
		Collector.__init__(self, "Snort")
		self.add_param(StringParam('logfile', '/var/log/snort/alert', 'File containing the snort alert messages'))
		self.size  = 0
		
	def connect(self):
		self.size = os.path.getsize(self.logfile)
	
	def close(self): 
		pass
		
	def reset(self):
		Collector.reset(self)
		self.size = os.path.getsize(self.logfile)
		
	def _read_alerts(self):
		alerts = []
		alert  = []
		f = open(self.logfile)
		f.seek(self.size)
		lines  = f.readlines()
		self.size = os.path.getsize(self.logfile)
		f.close()
		for l in lines:
			if l[:4] == "[**]":
				if len(alert) > 0:
					alerts.append(alert)
				alert = []
			alert.append(l)
		if len(alert) > 0:
			alerts.append(alert)
		return alerts
	
	def correlate(self, exploits):
		alerts = self._read_alerts()
		for e in exploits:
			if self.results.has_key(e.number) == False:
				self.results[e.number] = []

		for a in alerts:
			p = self._get_port(a)
			found = False
			for e in exploits:
				#print "Port %d (exploit range is %d-%d)"%(p,e.tcp_ports[0],e.tcp_ports[1])
				if p >= e.tcp_ports[0] and p <= e.tcp_ports[1]:
					self.results[e.number].append(string.join(a,""))
					found = True
					break
			if not found:
				self.results["uncorrelated"].append(string.join(a,""))
				
	def _get_port(self, alert):
		for l in alert:
			i = l.find(" -> ")
			if i > 0:
				s = l.rfind(":",0,i)
				try:
					res = int(l[s+1:i])
					return res
				except:
					print "[Snort] Error converting: %s"%l
		return -1


