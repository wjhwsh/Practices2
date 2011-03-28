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
IPLastFirst
------------
  Switch the first and the last packets
'''
from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip

class IPLastFirst(IPLayerOperator):
 	isa_operator      = True  
 	
 	def __init__(self):
 		IPLayerOperator.__init__(self,'IPLastFirst','Puts the last fragment(MF=0) in first position')	
 		
 	def mutate(self, packets):
 		if len(packets) < 2:
 			return packets
 		
 		last = len(packets)
 		packets.insert(0,packets[last-1])
 		del(packets[last])
 		return packets
 	
 		
