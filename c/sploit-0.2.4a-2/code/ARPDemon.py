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
# $Id: ARPDemon.py 111 2006-03-01 20:29:47Z balzarot $



import socket, os, time, sys
import scapy.scapy as scapy
import logger

class ARPDemon:
	'''
	Reverse ARP demon.
	'''

	def __init__(self, fakeip, macaddr, iface='eth0'):
		'''
		Replies to all the ARP requests about $ethaddr with the $ethaddr 
		'''
		self.log = logger.main.newSource("ARP-Demon")
		self.fakemac  = macaddr
		self.iface    = iface
		self.fakeip   = fakeip
		msg1 = "Reverse ARP demon creation...\r\n"
		msg2 = "    Interface: %s\r\n"%self.iface
		msg3 = "    Fake IP  : %s\r\n"%self.fakeip
		msg4 = "    Fake MAC : %s\r\n"%self.fakemac
		self.log.info(msg1+msg2+msg3+msg4)
		
		self.demon_pid = 0

		self.rsocket = None
		try:
			self.wsocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(scapy.ETH_P_ALL))
		except:
			self.log.error('Unable to open a packet socket for output.\r\nDo you have the right permissions?')
		
		self.answer = scapy.Ether(src=self.fakemac)/scapy.ARP(op='is-at', hwsrc=self.fakemac, psrc=fakeip)
		
		self.log.info("Initialization completed")
	
	def main_loop(self):
		self.log.info("Demon start processing incoming ARP request...")
		while 1:
			p = self.rsocket.recv(1600)
			self.process(p)

	def process(self, packet):
		self.log.debug('Process packet')
		arp = packet.payload
		if arp.name != 'ARP':   # Spourius packet
			self.log.warning(' Spourius Packet')
			return
		if arp.op == 1 and arp.pdst == self.fakeip:
			try:
				self.answer.dst = packet.src
				self.wsocket.sendto(str(self.answer),(self.iface,scapy.ETH_P_ALL))
				self.log.debug('rcv: %s'%arp.summary())
				self.log.debug('  sent fake response')
			except socket.error,msg:
				print msg

	def is_running(self):
		if self.demon_pid==0:
			return False
		else:
			return True
			
	def stop(self):
		os.kill(self.demon_pid,9)
		self.log.info("Demon stopped")
		self.demon_pid = 0

	def start(self):
		self.log.info("Starting ARP daemon on %s"%self.iface)
		self.rsocket  = scapy.L2ListenSocket(iface=self.iface, promisc=True, filter='arp')
		pid = os.fork()
		if pid == 0:
			self.main_loop()
		elif pid < 0:
			self.log.error("fork error")
		else:
			self.demon_pid=pid

	def bpoison(self, targetip, n=10, interval=10):
		p = scapy.Ether(src=self.fakemac , dst='ff:ff:ff:ff:ff:ff')/scapy.ARP(op="who-has", hwsrc=self.fakemac, psrc=self.fakeip, pdst=targetip)
		for x in range(n):
			scapy.sendp(p)
			time.sleep(interval)
		
if __name__ == '__main__':
	print "Testing ARPDaemon..."
	if len(sys.argv) < 3:
		print "Use %s <FakeIP> <FakeMAC> [iface]"%sys.argv[0]
		sys.exit()
	if len(sys.argv) == 4:
		d = ARPDemon(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		d = ARPDemon(sys.argv[1], sys.argv[2])
	d.log.setLevel(0)
	try:
		d.start()
		d.main_loop()
	except Exception, e:
		print e
		d.stop()
	print "End of testing"
		

