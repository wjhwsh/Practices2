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
# $Id: HTTP-HeaderChangeCase.py 109 2006-02-27 20:17:42Z balzarot $

import string
from HTTPLayerOperator import HTTPLayerOperator

class HTTPHeaderChangeCase(HTTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		HTTPLayerOperator.__init__(self,'HeaderChangeCase', 'Change the case for every keys in the header')	
				
	def mutate(self, requests):
		result = []
		for r in requests:
			temp = {}
			for key,item in r.header.iteritems():
				key2 = self.changecase(key)
				temp[key2]=item
			r.header = temp
			result.append(r)
		return result
		

	def changecase(self, s):
		result = ""
		ff = False
		for c in s:
			if ff:
				ff = False
				result += c
			else:
				ff = True
				result += string.swapcase(c)
		return result