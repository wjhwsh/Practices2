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
TCPOutOfOrder2
 It randomly shuffle the list of packets
'''

from TCPLayerOperator import TCPLayerOperator
import random


class TCPOutOfOrder2(TCPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		TCPLayerOperator.__init__(self,'TCPOutOfOrder2','TCP segments sent out of order')	
						
	def mutate(self, packets):
					
		if len(packets) == 1:
			return packets
				
		random.seed()
		random.shuffle(packets)						
		return packets

