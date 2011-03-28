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
# $Id: HTTP-PrematureEnding.py 109 2006-02-27 20:17:42Z balzarot $

from HTTPLayerOperator import HTTPLayerOperator
from interfaces.hasparameters import StringParam

class HTTPPrematureEnding(HTTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		HTTPLayerOperator.__init__(self,'PrematureEnding', 'see whisker for details')	
		self.add_param(StringParam('DIR','/','Fake directory inserted at the beginning', isMultiValues=True))
		
	def mutate(self, requests):
		result = []
		for r in requests:
			temp = self.DIR+"%20HTTP/1.0%0d%0aHeader:%20/../.."+r.url
			r.url = temp
			result.append(r)
		return result
		
