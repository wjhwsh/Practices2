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
IPRetarder
------------
 This operator retards one of the fragment of a certain amount of seconds.
 The IDS will be evaded if the reassembly timeout of the IDS is shorter 
 than the delay value but the timeout on the target is longer.
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPRetarder(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPRetarder','IP Fragmenter with timeouts')	
		#ultimo parametro valore minimo
		self.add_param(IntParam('numfrag',3,'Fragment to delay',2))
		self.add_param(IntParam('timer',18,'Timeout',1))
		
	def mutate(self, packets):
		timer = self.timer
		numfrag = self.numfrag
		
		# Check there is enough fragments
		if numfrag > len(packets):
			return packets
		
		# Check that the packets to delay it is actually a fragmet
		if packets[numfrag-1].flags % 2 != 1:
			return packets
		#set the timeout		
		packets[numfrag-1].timeout = timer
					
		return packets

