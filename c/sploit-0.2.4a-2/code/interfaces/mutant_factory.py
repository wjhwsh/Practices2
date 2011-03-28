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
# $Id: mutant_factory.py 109 2006-02-27 20:17:42Z balzarot $


from hasparameters import HasParameters

class MutantFactory(HasParameters):
	
	def __init__(self, name=""):
		self.opmanager = None       # Mutant operators manager
		self.name      = name
		
	def get_name(self):
		return self.name
		
	def set_opmanager(self, opmanager):
		self.opmanager = opmanager
		self.reset()
	
	def set_first(self, firstmutant):
		'''Set the index of the first mutant that have to be generated
		
		@firstmutant = the index of the first mutant to be generated
		'''
		return False
	
	def require_sync_collectors(self):
		"""Return True if the factory needs the alerts list to compute the
		   next exploit. False otherwise
		"""
		return False
	
	def reset(self):
		'''Reset the counter. The generation will restart from the beginning
		   This function is called each time the opmanager is modified
		'''
		pass

	def next(self, result):
		'''Returns the set of mutant operators for the next mutant
		
		@result = result of the previous mutant
		
		Return a list of mutant operators to use to generate the next mutant 
		or None if there are no other mutant.
		'''
		return None

	def count(self):
		'''Returns the number of possible mutants'''
		return 0
	
	def current(self):
		'''Returns the index of the current mutant'''
		return 0
	
