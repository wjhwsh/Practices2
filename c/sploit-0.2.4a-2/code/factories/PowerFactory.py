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
# $Id: PowerFactory.py 109 2006-02-27 20:17:42Z balzarot $

from interfaces.mutant_factory import MutantFactory

class PowerFactory(MutantFactory):
	
	def __init__(self):
		MutantFactory.__init__(self)
		self.reset()
		
	def set_first(self, mutantnumber):
		if mutantnumber >= 0 and mutantnumber < self.number:
			self.current = mutantnumber
			return True
		return False

	def reset(self):
		self.current = 0
		self.number  = 0
		if self.opmanager == None:
			return
		
		self.number  = 1
		self.selected = self.opmanager.get_selected_operators()
		for y in self.selected:
			self.number *= (1+y.params_combinations())

	def next(self, result):
		if self.opmanager == None:
			return None
		
		if (self.current >= self.number):
			return None
		result = []
		n = self.current
		for y in self.selected:
			value = n % (1+y.params_combinations())
			#print "N = %d C = %d Value = %d"%(n,y.params_combinations(),value)
			if value > 0:
				if value > 1:
					y.set_params_combination(value-1)
				result.append(y)
			n = n / (1+y.params_combinations())
		self.current += 1
		return result

	def count(self):
		return self.number

	def current(self):
		return self.current



