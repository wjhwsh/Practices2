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

# Author: Andrea Beretta and Riccardo Bianchi
# $Id$

'''
TCPOutofOrder
 Switch the position of two packets
'''

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import utils

class TCPOutofOrder(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=1):
		TCPLayerOperator.__init__(self,'TCPOutofOrder','TPC packet swapped with the next')	
		self.add_param(IntParam('numseg',2,'Segment to be swapped',1))
		
					
	def mutate(self, packets):
		numseg = self.numseg
		
		#Not enough segments, Syn or Ack, return
		if utils.check_length(numseg, packets) or utils.check_syn(packets[numseg-1]) or utils.check_ack(packets[numseg-1]):
			return packets
			
		packets.insert(numseg+1, packets[numseg-1])
		del(packets[numseg-1])
		
		return packets

