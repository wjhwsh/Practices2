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
# $Id: ip.py 130 2006-05-03 15:33:04Z balzarot $

import array
import scapy.scapy as scapy
import random
import string
 
import logger

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO: gestire le opzioni 
# TODO: gestire timer per i frammenti
# TODO: gestire parametri di default 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                            IP FLAGS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FLAG_MF       = 1  # More fragment (this is not the last fragment)
FLAG_DF       = 2  # Don't fragment
FLAG_RESERVEd = 4  # For future use
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         DEFAULT VALUES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DEFAULT_TARGET_ADDR    = '127.0.0.1'
DEFAULT_SOURCE_ADDR    = '127.0.0.1'
DEFAULT_IP_OPERATORS = []
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                       FRAGMENTATION ROUTINES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def fragment(packet, size):
	data     = str(packet.payload)
	data_len = len(data)
	size  = size/8*8  # the size of each fragment must be a multiple of 8
	if size < 1:
		return None   # no fragment less than 8 byte
	n_frag = data_len / size
	if data_len > (n_frag*size):
	    n_frag += 1
	if n_frag == 1:
		return [packet]

	#print "Fragmenting %d in %d pieces of %d bytes"%(data_len, n_frag, size)
	# start fragmentation
	result = []	
	frag = packet.copy()
	proto = frag.proto
	del(frag.payload)
	
	for n in range(n_frag):
		f = frag.copy()
		f.add_payload(scapy.Raw(load=data[n*size:(n+1)*size]))
		f.frag = n*size/8
		f.proto = proto
		if hasattr(packet, "timeout") and n==0:
			f.timeout = packet.timeout
		if n!=(n_frag-1): 
			f.flags = FLAG_MF
		else:
			f.flags = 0
		result.append(f)
	#for p in result: p.display()
	return result	

def reassembly(fragments):
	l = IPFragList(0,0,0)
	for p in fragments:
		l.add(p)
	return l.reassembly()
	
class IPFragManager:
	def __init__ (self, ip_id, ip_proto, timer):
		''' Initialize the reassembly queue. Each queue is indentified by the id of the
	    packet and the protocol. (and ip_src - ip_dest but here they are obvious)
		'''
		self.ip_id       = ip_id
		self.ip_proto    = ip_proto
		self.list        = []
		self.timer       = timer
		self.complete    = False
		self.overlapping = False
		self.log         = logger.main.newSource("IP (frag manager)")
		
	def add(self, packet):
		# search the position where the packet has to be inserted
		pos = 0
		for p in self.list:
			if packet.frag < p.frag:
				break
			pos += 1
		
		self.log.debug("Fragment at position = %d"%pos)
		
		data  = str(packet.payload)
		start = packet.frag*8
		end   = start + len(data)
		
		# check possible overlapping with packets at left
		if (pos > 0):
			prec = self.list[pos-1]
			i = prec.frag*8 + len(prec.payload) - start
			if i > 0: # overlapping
				self.log.debug("Left overlapping of %d bytes"%i)
				self.overlapping = True
				if i >= len(data): #complete overlapping --> drop packet
					return
				# partial overlapping, cut the data
				data = data[i:]
				packet.frag += i/8
				packet.payload.load = data
		
		# check possible overlapping with packets at right
		cursor = pos
		while cursor < len(self.list):
			next = self.list[cursor]
			i = end - next.frag*8
			if i <= 0:	# no overlapping
				break
			self.log.debug("Right overlapping of %d bytes"%i)
			self.overlapping = True
			next_data = str(next.payload)
			if i < p.frag*8+len(next_data): 
				# partial overlapping, cut the data
				next_data = next_data[i:]
				next.frag += i/8
				next.payload.load = data
				break
			# complete overlapping -> drop next packet
			del(self.list[cursor])
				
		self.list.insert(pos,packet)
		
		# check if all fragments have arrived
		if (self.list[-1].flags & FLAG_MF):
 			return
		next_frag = 0
		for p in self.list:
			if p.frag != next_frag:
				# There is a hole: a packet is missing
				return
			next_frag += len(p.payload)/8
		# Ok, all the fragments have been received 
		self.complete = True
			 
	def reassembly(self):
		if self.complete == None:
			return None
		
		res = self.list[0].copy()
		del(res.payload)
		res.flags = 0
		res.frag  = 0
		
		data = array.array('c')
			
		for f in self.list:
			data.fromstring(str(f.payload))
	
		res.do_dissect_payload(data.tostring())
		return res			


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         IP MANAGER 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IPManager:
	ip_id = 1;
	
	def __init__(self, saddr=None, daddr=None):
		if saddr: 
			self.saddr = saddr
		else:
			self.saddr = DEFAULT_SOURCE_ADDR
	
		if daddr: 
			self.daddr = daddr
		else:
			self.daddr = DEFAULT_TARGET_ADDR
		
		self.filters   = DEFAULT_IP_OPERATORS
		self.frag_list = []
		self.log       = logger.main.newSource("IP")
		
		# default value of ip fields
		self.ttl 	 		   = 64 		# default time to live
		self.id	= random.randint(1,65535)	# First packet ID
		self.per_protocol_id   = False	    # use unique id for each protocol
		self.reassembly_timout = 60			# timeout for the reassembly routine

		# ip statistics
		self.stat_no_frag     = 0
		self.stat_packets     = 0
		self.stat_invalid     = 0
		self.stat_fragover    = 0
		
	def nextID(self):
		self.id += 1
		if self.id > 65535:
			self.id = 1 
		return self.id
			
	def add_filter(self, eth_filter):
		self.filters.append(eth_filter)
		
	def encapsulate(self, packets):
		if type(packets) != list:
			fragment = (scapy.IP(src=self.saddr , dst=self.daddr, id=self.nextID(), ttl=self.ttl)/packets)			
			if hasattr(packets, "timeout"):
				fragment.timeout = packets.timeout
			return [fragment]
		else:
			fragments = []
			for p in packets:
				fragment = (scapy.IP(src=self.saddr , dst=self.daddr, id=self.nextID(), ttl=self.ttl)/p)
				if hasattr(p, "timeout"):
					fragment.timeout = p.timeout
				fragments.append(fragment)
			return fragments
	
	def process_out(self, packets):
		if packets==None or len(packets)==0:
			return None
		
		temp = self.encapsulate(packets)
		for mf in self.filters:
			temp = mf.mutate(temp)
		return temp
	
	def validate(self, packet):
		if(packet.src != self.daddr) or (packet.dst != self.saddr):
			# spourious packet
			self.log.warning("Spourious packet")
			return False
		return True	
		
	def process_in(self, packet):
		self.stat_packets += 1		
		if self.validate(packet) == False:
			self.stat_invalid += 1
			return None
		if (packet.flags & FLAG_MF) or (packet.frag > 0):
			self.log.debug("Packet fragmented")
			pos = 0
			man = None
			for fm in self.frag_list:
				if (fm.ip_id == packet.id) and (fm.proto == packet.proto):
					man = fm
					break
				pos += 1
			if man==None:
				man = IPFragManager(packet.id,packet.proto,0)
				self.frag_list.append(man)
			man.add(packet)
			if man.complete:
				self.stat_no_frag += 1
				if man.overlapping: self.stat_fragover += 1
				result = man.reassembly()
				del(self.frag_list[pos])
				return result
			else:
				return None
		else:
			return packet.payload
			
	def log_stats(self):
		self.log.info("Statistics:\r\n Packets: %d\r\n Received Fragments: %d (%d overlapping)\r\n Invalid: %d"%(self.stat_packets, self.stat_no_frag, self.stat_fragover, self.stat_invalid))
	

