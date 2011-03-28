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
IP_Big_mtu
------------
 A new packet is inserted into the traffic whit a big size and the DF (don't fragment) flag set.
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import scapy.scapy as scapy
import random
import string
import utils

class Big_mtu(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IP_Big_mtu','IP Fragmenter with large MTU')	
		self.add_param(IntParam('bigsize',1300,'Size of the big fragment',20))
		self.add_param(IntParam('numfrag',3,'Fragment to evade',1))
			
	def mutate(self, packets):
		numfrag = self.numfrag
		bigsize = self.bigsize
		big_payload=""
		
		#check numfrag existence, and if it's a fragment
		if utils.check_length(numfrag, packets) or not utils.check_fragmentation(packets[numfrag-1]):
			return packets 

		#create big payload and load it		
		forged = packets[numfrag-1].copy()
		del(forged.payload)
		for i in range(bigsize):
			big_payload =big_payload + random.choice(string.ascii_letters)
		forged.add_payload(scapy.Raw(load=big_payload))
		forged.flags = ip.FLAG_DF
		#insert big packet	
		packets.insert(numfrag-1, forged)

		return packets


