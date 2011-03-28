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
# $Id: NullFactory.py 109 2006-02-27 20:17:42Z balzarot $

from interfaces.mutant_factory import MutantFactory

class NullFactory(MutantFactory):
	
	def __init__(self):
		MutantFactory.__init__(self, "Null Factory")
		self.current  = 0
		self.number   = 1
			
	def set_first(self, mutantnumber):
		if mutantnumber == 0:
			return True
		return False
		
	def reset(self):
		self.current = 0
				
	def next(self, result):
		if (self.current > 0):
			return None
		
		self.current = 1
		return {}

	def count(self):
		return 1

	def current(self):
		return self.current

