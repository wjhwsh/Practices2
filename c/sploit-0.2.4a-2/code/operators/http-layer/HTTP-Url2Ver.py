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
# $Id: HTTP-Url2Ver.py 109 2006-02-27 20:17:42Z balzarot $

from HTTPLayerOperator import HTTPLayerOperator
from interfaces.hasparameters import StringParam

class HTTPUrl2Ver(HTTPLayerOperator):
	
	isa_operator      = True  
	
	def __init__(self):
		HTTPLayerOperator.__init__(self,'Url2Version','Change the separator character between the URL and the HTTP version')	
		param = StringParam('CHAR',' \t','Character to be used as separator', isMultiValues=True)
		param.set_multiple_values(['	','\t','  \t'])
		self.add_param(param)
	
	def mutate(self, requests):
		result = []
		for r in requests:
			r.url2version = self.CHAR
			result.append(r)
		return result
		
