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
# $Id: HTTP-UrlHexEncoder.py 109 2006-02-27 20:17:42Z balzarot $

from HTTPLayerOperator import HTTPLayerOperator
import string, binascii

def hexEncoder(s):
	result = ""
	jump = 0
	for c in s:
		if jump > 0:
			jump = jump - 1
			result = result + c
		elif c == "%":
			jump = 2
			result = result + c
		else:
			result = result + "%" + binascii.hexlify(c)
	return result
			
class HTTPUrlHexEncoder(HTTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		HTTPLayerOperator.__init__(self,'URLHexEncoder', 'Encode the URL text')	
	
	def encode(self, url):
		temp = string.split(url,"/")
		result = ""
		for t in temp:
			result = result + hexEncoder(t) + "/"
		return result[:-1]
		
	def mutate(self, requests):
		result = []
		for r in requests:
			r.url = self.encode(r.url)
			result.append(r)	
		return result
		
