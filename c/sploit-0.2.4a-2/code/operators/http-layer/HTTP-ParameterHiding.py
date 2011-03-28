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
# $Id: HTTP-ParameterHiding.py 109 2006-02-27 20:17:42Z balzarot $

from HTTPLayerOperator import HTTPLayerOperator
from interfaces.hasparameters import StringParam

class HTTPParameterHiding(HTTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		HTTPLayerOperator.__init__(self,'ParameterHiding', 'see whisker for details')	
		self.add_param(StringParam('DIR','/','Character to be inserted', isMultiValues=True))
		
	def mutate(self, requests):
		result = []
		for r in requests:
			temp = self.DIR+"%3fparam=/.."+r.url
			r.url = temp
			result.append(r)
		return result
		
