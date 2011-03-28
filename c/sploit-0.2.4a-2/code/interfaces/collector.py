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
# $Id: collector.py 109 2006-02-27 20:17:42Z balzarot $

from hasparameters import HasParameters

class Collector(HasParameters):
	'''Defines the interface for the collector classes '''
	
	def __init__(self, idsname):
		HasParameters.__init__(self)
		self.ids_name = idsname
		self.results = {"uncorrelated":[]}
		
	def connect(self, target):
		''' 
		'''
		pass
	
	def get_name(self):
		return self.ids_name
	
	def close(self): 
		'''
		'''
		pass			
	
	def reset(self):
		'''
		'''
		self.results = {"uncorrelated":[]}

	def get_alerts(self, mutant_number=None):
		'''
		Return the alerts correlated to the mutant mutant_number
		If mutant_number is None (that is the default value) the function
		returns the whole alerts table
		'''
		if mutant_number == None:
			return self.results
		elif self.results.has_key(mutant_number):
			return self.results[mutant_number]
		else:
			return None
		
		
	def correlate(self, exploits):
		pass
