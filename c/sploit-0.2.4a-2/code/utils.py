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
# $Id: utils.py 50 2005-11-02 14:29:24Z balzarot $

import sys, os
import scapy.scapy as scapy
import managers.ip as ip
import managers.tcp as tcp
import random
import string
from interfaces.mutant_factory import MutantFactory
from interfaces.collector import Collector

NOPAYLOAD = 1

def load_collectors_list(path="."):
	sys.path.append(path)
	result = []
	for f in os.listdir(path):
		if f[-3:] == ".py":
			module  = __import__(f[:-3]) 
			content = dir(module)
			for x in content:
				try:
					obj = module.__dict__[x]
					if issubclass(obj,Collector):
						try:
							temp = obj()
						except Exception, msg:
							pass
							#print "ERROR loading alert collector %s:%s"%(obj,msg)
						result.append(temp)
				except Exception, msg:
					pass
	sys.path.remove(path)
	return result

def load_collector(file):
	path, filename = os.path.split(file)
	sys.path.append(path)
	result = []
	if filename[-3:] == '.py':
		module  = __import__(filename[:-3])
	elif filename[-4:] == '.pyc':
		module  = __import__(filename[:-4])
	content = dir(module)
	for x in content:
		try:
			obj = module.__dict__[x]
			if issubclass(obj,Collector):
				temp = None
				try:
					temp = obj()
					sys.path.remove(path)
					return temp
				except Exception, msg:
					#print "ERROR loading alert collector %s:%s"%(obj,msg)
					pass
		except Exception, msg:
			pass
	sys.path.remove(path)
	return None

def load_factory(file):
	path, filename = os.path.split(file)
	sys.path.append(path)
	if filename[-3:] == '.py':
		module  = __import__(filename[:-3])
	elif filename[-4:] == '.pyc':
		module  = __import__(filename[:-4])
	content = dir(module)
	for x in content:
		if x == "MutantFactory": continue
		try:
			obj = module.__dict__[x]
			if issubclass(obj,MutantFactory):
				try:
					res = obj()
					sys.path.remove(path)
					return res
				except Exception, msg:
					print "Error during factory instantiation: %s"%msg
		except Exception, msg: 
			pass
	sys.path.remove(path)
	return None

#rewrite packet or fragment payload
#aggiungere controllo se pacchetto o frammento		
def ip_bad_payload(packet, options = 0):
	random.seed()
	bad_payload = ""
	l = 0
	#vedo se frammento contiene header di pacchetto tcp
	if(packet.haslayer(scapy.TCP)):
		if (options & NOPAYLOAD) == 0:	
			tcp = packet.payload
			#calcolo lungh. payload tcp
			l = len(str(tcp.payload))
			for i in range(l):
				bad_payload = bad_payload + random.choice(string.ascii_letters)
			#delete tcp_payload	
			del(tcp.payload)
			#aggiungo nuovo payload tcp
			tcp.add_payload(scapy.Raw(load=bad_payload))					
			#cancello segmento tcp incapsulato in packet
			del(packet.payload)
			#carico nuovo segmento tcp in packet
			packet.add_payload(tcp)		
			#In alternativa potrei decidere di non fare nulla e ritornare il pacchetto tcp		
			#return packet
		else:
			#only delete tcp payload
			del(packet.payload.payload)	
	else:
		#pacchetti IP, non incapsula header tcp
		if (packet.haslayer(scapy.Raw)):
			data = packet.payload
			l = len(str(data))
			del(data)
			for i in range(l):		
				bad_payload = bad_payload + random.choice(string.ascii_letters)
			del(packet.payload)
			packet.add_payload(scapy.Raw(load=bad_payload))	

	return packet
	
	
#rewrite segment payload
# TODO: vedere se si puo' fondere col precedente
def tcp_bad_payload(segment, options = 0):
	random.seed()
	bad_payload = ""
	l = 0
	if(segment.haslayer(scapy.TCP)):
		l = len(str(segment.payload))
		#delete tcp_payload	
		del(segment.payload)		
		
		if (options & NOPAYLOAD) == 0:		
			for i in range(l):
				bad_payload = bad_payload + random.choice(string.ascii_letters)
			#aggiungo nuovo payload tcp
			segment.add_payload(scapy.Raw(load=bad_payload))					

	return segment
	
#length check
def check_length(pos, packets):
	if pos >= len(packets):
		return True
	else:
		return False	

#syn check
def check_syn(packet):
	if ( packet.haslayer(scapy.TCP) and hasattr(packet, "flags") and (packet.flags & tcp.FLAG_SYN) ):
		return True
	else:
		return False

#ack check		
def check_ack(packet):
	if ( packet.haslayer(scapy.TCP) and hasattr(packet, "flags") and (packet.flags & tcp.FLAG_ACK) and not hasattr(packet, "load") ):
		return True
	else:
		return False

#fragment check
def check_fragmentation(packet):
	if ( packet.frag > 0 or (packet.flags &	ip.FLAG_MF) ):
		return packet 
	else:
		return False

#l4manager existence check
def check_l4m(packets):
	for p in packets:
		if hasattr(p, "l4manager"):		
			return p.l4manager
	return None	




