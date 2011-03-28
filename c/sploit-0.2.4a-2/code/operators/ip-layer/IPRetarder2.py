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
IPRetarder2
------------
 A fragment containing wrong data is put at the beginnning of the list
 A long delay time is set between the first (the wrong) and the second fragment
 If the delay is longer than the reassembly timeout of the target it should discart 
 it and start reassebling the traffic from the second packet
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPRetarder2(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPRetarder2','IP Fragmenter with timeouts and false payload')	
		#ultimo parametro valore minimo
		self.add_param(IntParam('numfrag',3,'Fragment to delay',2))
		self.add_param(IntParam('timer',33,'Timeout - must be > of host\'s ipfrag_time',1))
		
	def mutate(self, packets):
		timer = self.timer
		numfrag = self.numfrag
						
		# Check there is enough fragments
		if numfrag > len(packets):
			return packets
		
		# Check that the packets to delay it is actually a fragmet
		if packets[numfrag-1].flags % 2 != 1:
			return packets
		
		forged = packets[numfrag-1].copy()
		forged = utils.ip_bad_payload(forged)
		#insert forged		
		packets.insert(0,forged)
		#append original one
		packets.append(packets[numfrag])
		del(packets[numfrag])
		#set timeouts		
		packets[1].timeout = timer
		last=len(packets)-1
		packets[last].timeout = 2
	
		return packets




