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
TCPBadFlags
 Copy a tcp segment, add a random payload, and set a not-allowed combination
 of tcp flags.
'''

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
from interfaces.hasparameters import KeyListParam
import utils

class TCPBadFlags(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=1):
		TCPLayerOperator.__init__(self,'TCPBadFlags','TCP packet with bad flags configuration')	
		self.add_param(IntParam('numseg',5,'Segment with bad flag and payload',1))
		#FSRPAU			
		flags_conf = [ "F", "U", "FS", "SR", "FR", "FRA", "FRPA", "FSP", "FSR", "FSRP" ]
		self.add_param(KeyListParam('flags',flags_conf[3], flags_conf, 'TCP flags for bad segment'))
		pos_list = ["before", "after", "last"]
		self.add_param(KeyListParam('position',pos_list[0], pos_list, 'position of overlapping segment => before | after | last'))

	def mutate(self, packets):
		numseg = self.numseg
		position = self.position
		flags_ = self.flags
		#do nothing
		if utils.check_length(numseg, packets) or utils.check_syn(packets[numseg-1]) or utils.check_ack(packets[numseg-1]):
			return packets
			
		forged = packets[numseg-1].copy()
		forged = utils.tcp_bad_payload(forged)
		forged.flags = flags_
		
		if position == "after":
			packets.insert(numseg, forged)
		elif position == "before":	
			packets.insert(numseg-1, forged)
		else:
			packets.append(packets[numseg-1])
			del(packets[numseg-1])
			packets.insert(numseg-1, forged)	
		
		return packets

