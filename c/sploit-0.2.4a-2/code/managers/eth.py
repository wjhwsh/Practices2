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

import os
import scapy.scapy as scapy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         DEFAULT VALUES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DEFAULT_TARGET_MAC = '00:00:00:00:00:00'
DEFAULT_SOURCE_MAC = '00:00:00:00:00:00'
DEFAULT_ETH_OPERATORS = []

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
class EthManager:
	
	def __init__(self, smac=None, dmac=None):
		if smac:
			self.smac = smac
		else:
			self.smac = DEFAULT_SOURCE_MAC
		if dmac:
			self.dmac = dmac
		else:
			self.dmac = DEFAULT_TARGET_MAC
			
		self.filters = DEFAULT_ETH_OPERATORS
	
	def add_filter(self, eth_filter):
		self.filters.append(eth_filter)
		
	def encapsulate(self, packets):
		if type(packets) != list:
			frame = (scapy.Ether(src=self.smac , dst=self.dmac)/packets)			
			if hasattr(packets, "timeout"):
				frame.timeout = packets.timeout			
			return [frame]
		else:
			frames=[]
			for p in packets:			
				frame = (scapy.Ether(src=self.smac, dst=self.dmac)/p)
				if hasattr(p, "timeout"):
					frame.timeout = p.timeout
				frames.append(frame)
			return frames
	
	def validate(self, packet):
		#if packet with fake MAC drop it
		if packet.dst != self.smac.lower() and packet.dst != self.dmac.lower():
			return False
		return True
			
	def process_out(self, packets):
		if packets==None or len(packets)==0:
			return []
		temp = self.encapsulate(packets)
		for mf in self.filters:
			temp = mf.mutate(temp)
		return temp

	def process_in(self, packet):
		if self.validate(packet) == False:
			return None
		return packet.payload

