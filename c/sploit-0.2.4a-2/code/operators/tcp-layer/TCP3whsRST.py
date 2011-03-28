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
# $Id: __init__.py 50 2005-11-02 14:29:24Z balzarot $


'''
TCP3whsRST
al passaggio dell\'ACK del primo 3whs, vengono creati e appesi un RESET ed un nuovo SYN con iss aumentato in base
al parametro offset, allo scopo di resettare la prima connessione ed effettuarne una nuova. Ack e seq ricevuti ed
inviati vengono modificati di conseguenza; il flag post_syn del tcpmanager viene settato a true allo scopo di
processare il SYN-ACK anche con connessione established
''' 

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import scapy.scapy as scapy
import socket
import utils
import managers.tcp as tcp

class TCP3whsRST(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self):
		TCPLayerOperator.__init__(self,'TCP3whsRST','Reset conn. after 3whs and reconnect with different seq. numbers')	
		self.add_param(IntParam('offset',150000,'offset for seq. number', 1))
							
	def mutate(self, packets):
		offset = self.offset
		
		#find tcp manager reference, otherwise return packets
		l4m = utils.check_l4m(packets)
		if not l4m:
			return packets

			
		if ((packets[0].flags & tcp.FLAG_ACK) and (l4m.post_syn == 0)):
			
			rst = packets[0].copy()
			rst.flags = 'R'
			
			#syn
			syn = scapy.TCP(dport=l4m.dport, sport=l4m.sport, flags='S', seq=l4m.iss, window=l4m.rcv_wnd,\
					options=[('MSS', l4m.default_max_size)])
			
			# update seqs and akcs			
			l4m.sent_next_seq = l4m.iss + 1
			l4m.sent_last_ack = 0			
			l4m.rcv_last_ack = 0
			l4m.rcv_next_seq = 0		
									
			packets.append(rst)
			packets.append(syn)
			
			l4m.post_syn = 1
			
			return packets
												
		return packets



