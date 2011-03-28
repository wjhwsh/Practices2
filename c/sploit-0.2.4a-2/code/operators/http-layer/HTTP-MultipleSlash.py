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
# $Id: HTTP-MultipleSlash.py 109 2006-02-27 20:17:42Z balzarot $

from HTTPLayerOperator import HTTPLayerOperator
from interfaces.hasparameters import IntParam
import string

class HTTPDoubleSlash(HTTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		HTTPLayerOperator.__init__(self,'MultipleSlash', 'Change every slash with multiple slashes')	
		self.add_param(IntParam('N',2,'Number of slash to be used',1))
		
	def mutate(self, requests):
		result = []
		for r in requests:
			temp = string.replace(r.url,"/","/"*self.N)
			temp = temp.replace("\\","\\"*self.N)
			r.url = temp
			result.append(r)
		return result
		
