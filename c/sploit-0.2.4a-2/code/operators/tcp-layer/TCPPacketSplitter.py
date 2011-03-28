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
# $Id$

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import scapy.scapy

class TCPSplit(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=10):
		TCPLayerOperator.__init__(self,'TCP-Split','Split a TCP packet in multiple little packets')	
		self.add_param(IntParam('size',10,'Data size of each packet',1))
		self.size = size
			
	def split(self, p, size):
		result = []
		l4manager = p.l4manager	
		data = str(p.payload)
		if len(data) == 0:
			return [p]
		del(p.payload)
		
		n = len(data)
		x = 0
		
		while x<n:
			temp = p.copy()
			temp.add_payload(data[x:x+size])
			temp.seq += x
			if hasattr (p,"timeout"):
				temp.timeout = p.timeout
			temp.l4manager = l4manager
			result.append(temp)
			x += size
		
		return result
		
	def mutate(self, packets):
		result = []
		size = self.size
		
		for p in packets:
			result.extend(self.split(p,size))
		return result
		
