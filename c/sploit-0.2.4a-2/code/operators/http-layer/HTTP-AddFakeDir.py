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
# $Id: HTTP-AddFakeDir.py 109 2006-02-27 20:17:42Z balzarot $

from HTTPLayerOperator import HTTPLayerOperator
from interfaces.hasparameters import StringParam
import string

class HTTPAddFakeDir(HTTPLayerOperator):
	
	isa_operator      = True  # can be instanciated

	def __init__(self):
		HTTPLayerOperator.__init__(self,'AddFakeDirectory', 'Change every / with a //')	
		self.add_param(StringParam('DIR','xyz','Name of the fake directory', isMultiValues=False))
		
	def mutate(self, requests):
		result = []
		for r in requests:
			temp = string.replace(r.url,"/","/%s/../"%self.DIR)
			r.url = temp
			result.append(r)
		return result
		
