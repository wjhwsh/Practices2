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
# $Id: logger.py 110 2006-03-01 16:48:51Z balzarot $

# Python import
import sys, threading
from time import gmtime, strftime

DEBUG   = 1      # Used to print very verbose messages during debugging
INFO    = 2      # Used to print info about the current status
WARNING = 3      # Something bad, but the program doesn't stop.
ERROR   = 4      # Unrecoverable error

OFF     = 100    # Used to stop logging

dlevels = [
'DEBUG',
'INFO',
'WARNING',
'ERROR'
]

class Logger:
	"""
	Class to manage the message logging. 
	"""

	def __init__(self, output=sys.stderr):
		""" Initialize the Logger object 
			output: where the debug message will be written 
			        (by default is the standard error) 
		"""
		self.out      = output
		self.lock     = threading.Condition()
		self.sources  = {}
		self.defaults = {}
		self.default_level = 3

	def redirect(self, dest):
		self.lock.acquire()
		self.out = dest
		self.lock.release()

	def removeSource(self, logsource):
		if self.sources.has_key(logsource.name):
			sources = self.sources[logsource.name]
			if logsource in sources:
				sources.remove(logsource)
		
	def getSources(self):
		return self.sources
	
	def newSource(self, name):
		if self.defaults.has_key(name):
			level = self.defaults[name]
		else:
			level = self.default_level
		temp = LogSource(name, level, self)
		if self.sources.has_key(name):
			self.sources[name].append(temp)
		else:
			self.sources[name] = [temp]
		return temp
	
	def write(self, message):
		self.lock.acquire()
		self.out.write(message)
		self.lock.release()
		
	def setLevel(self, lev, source=None):
		if source==None:
			self.default_level = lev
			for name, s in self.sources.items():
				for x in s:
					x.setLevel(lev)
			self.defaults = {}
		else:
			for name, s in self.sources.items():
				if name == source:
					for x in s:
						x.setLevel(lev)
					break
			self.defaults[source]=lev

class LogSource:
	"""
	Class to manage the message logging. 
	"""
	
	def __init__(self, name,  level, logger=None):
		""" Initialize the debug object 
				name:   mnemonic string that represents the entity that generates 
				        the messages. 
				level:  threashold level. A message will be logged if its level is
				        bigger than the threashold.
				output: the logger in charge to write the messages 
		"""
		self.dlevel = level
		self.out    = logger
		self.name   = name
		self.info("New Log Source: %s"%name)
			
	
	def setLevel(self, lvl):
		"""Set the threasold value"""
		self.dlevel = lvl
		
	def getLevel(self):
		"""Return the threasold level"""
		return self.dlevel
			
	def error(self, message):
		"""Shortcut used for error messages (level 4)"""
		if (self.dlevel > 4): return
		self.out.write("-[%s]--[%s]--------[%s]-\r\n%s\r\n"%(self.name, 'ERROR', strftime("%a, %d %b %Y %H:%M:%S", gmtime()),message))

	def warning(self, message):
		"""Shortcut used for warning messages (level 3)"""
		if (self.dlevel > 3): return
		self.out.write("-[%s]--[%s]--------[%s]-\r\n%s\r\n"%(self.name, 'WARNING', strftime("%a, %d %b %Y %H:%M:%S", gmtime()),message))

	def info(self, message):
		"""Shortcut used for informative messages (level 2)"""
		if (self.dlevel > 2): return
		self.out.write("-[%s]--[%s]--------[%s]-\r\n%s\r\n"%(self.name, 'INFO', strftime("%a, %d %b %Y %H:%M:%S", gmtime()),message))

	def debug(self, message):
		"""Shortcut used for debug messages (level 1)"""
		if (self.dlevel > 1): return
		self.out.write("-[%s]--[%s]--------[%s]-\r\n%s\r\n"%(self.name, 'DEBUG', strftime("%a, %d %b %Y %H:%M:%S", gmtime()),message))
			

# ********************************************************************
#						Main Logger
# ********************************************************************

main = Logger()

# ********************************************************************


