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
EthBadMac
-----------
 This operators creates a copy of one of the frame and replaces its
 content with random bytes. The new frame has the IP address of the
 target but a wrong MAC address.

'''

from EthLayerOperator import EthLayerOperator
from interfaces.hasparameters import IntParam
from interfaces.hasparameters import StringParam
from interfaces.hasparameters import KeyListParam
#from hasparameters import StringParam
import utils

class EthBadMac(EthLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		EthLayerOperator.__init__(self,'BadMAC','Inject packet with a correct IP address but a bad MAC address')	
		self.add_param(StringParam('BADMAC','10:C1:C1:C1:C1:33','Mac address to be used'))
		self.add_param(IntParam('numframe',2,'Frame with bad Mac',1))

		
	def mutate(self, packets):
			
		numframe = self.numframe
		BADMAC = self.BADMAC

		
		if utils.check_length(numframe, packets) or utils.check_syn(packets[numframe-1].payload.payload) or utils.check_ack(packets[numframe-1].payload.payload):
			return packets
				
		forged = packets[numframe-1].copy()
		forged.payload = utils.ip_bad_payload(forged.payload)
		forged.dst=BADMAC
		#insert forged frame
		packets.insert(0, forged)
		#append original
		packets.append(packets[numframe])
		del(packets[numframe])
		
		return packets
		
