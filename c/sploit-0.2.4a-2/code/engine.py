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
# $Id: engine.py 112 2006-03-02 10:13:28Z balzarot $

import os, sys, os.path
import time

import scapy.scapy

import utils
from opmanager import OpManager
from managers import ip
from managers import tcp
from managers import eth
from ARPDemon import ARPDemon
import interfaces.exploit
from interfaces.mutant_operator import MutantOperator
from interfaces.mutant_factory import MutantFactory
from interfaces.collector import Collector
from execinfo import ExecInfo
import logger
from cparser import CParser

VERSION = "0.2.4-2 Alpha"

DEFAULT_EXPLOIT_OPERATORS = []

class Engine:
	
	def __init__(self):
		
		# reverse arp demon. Used to simulate the virtual host
		self.arp_demon     = None
		# the exploit currently loaded
		self.exploit       = None
		# the module containing the current exploit
		self.exp_module    = None
		# the interface used to generate and receive packets
		self.interface     = 'eth0'
		# Mutant operators manager
		self.opmanager     = OpManager()
		# List of alert collectors
		self.collectors    = []
		# Mutant factory
		self.factory       = None
		# True if the alerts must be collected after each mutant execution
		self.collect_sync  = False
		# True if the log messages must be redirected during the exploit execution
		self.redirect      = True
		
		self.virtualhost_mac = 'undefined'
		self.virtualhost_ip  = 'undefined'
		
		self.targethost_mac  = 'undefined'
		self.targethost_ip   = '127.0.0.1'
				
		self.log    = logger.main.newSource("ENGINE")
		
		# Load the default mutant factory
		self.set_factory(utils.load_factory("factories/NullFactory.py"))
 		
		# Load the mutant operators
		self.opmanager.load_operators()
		
		# Scapy configuration
		scapy.scapy.conf.padding = 0

	def clean_up(self):
		self.log.info("Cleaning up.\nBye Bye")
		if (self.arp_demon != None) and (self.arp_demon.is_running()):
			self.arp_demon.stop()
		if self.exploit:
			del self.exploit
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Alert Collectors	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	def get_selected_collectors(self):
		return self.collectors
	
	def add_collector(self, collector):
		if collector in self.collectors:
			return
		self.collectors.append(collector)
	
	def remove_collector(self, collector):
		try:
			self.collectors.remove(collector)
		except:
			pass
				
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Interfaces	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def get_interfaces(self):
		temp = scapy.scapy.get_if_list()
		temp.remove('lo')
		return temp

	def get_iface(self):
		return self.interface
	
	def set_iface(self, iface):
		self.interface = iface
		tcp.interface  = iface
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Mutant factories
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def set_factory(self, factory):
		if factory == None:
			self.log.error('Attempt to set Factory to "None".')
		self.factory = factory
		self.factory.set_opmanager(self.opmanager)
		if self.factory.require_sync_collectors():
			self.collect_sync = True
		else:
			self.collect_sync = False
		self.log.debug('Mutant Factory sets to: %s'%self.factory.__class__)
	
	def get_factory(self):
		return self.factory
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Hosts
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def setVirtualHost(self, tmac, smac, ipaddr):
		self.log.info('Virtual host: %s (%s)'%(ipaddr,smac))
		self.log.info('Target MAC: %s'%(tmac))
				
		self.virtualhost_mac = smac
		self.virtualhost_ip  = ipaddr

		self.targethost_mac  = tmac
		eth.DEFAULT_TARGET_MAC = tmac

		ip.DEFAULT_SOURCE_ADDR = ipaddr
		eth.DEFAULT_SOURCE_MAC = smac
		if (self.arp_demon != None) and (self.arp_demon.is_running()):
			self.arp_demon.stop()
		self.arp_demon = ARPDemon(ipaddr, smac, iface=self.interface)
		
	def start_demon(self):
		if self.arp_demon == None:
			self.log.error('Attempt to start the ARP demon before configuring it')
			return False
		if self.arp_demon.is_running()==False:
			 self.arp_demon.start()
		return True
	
	def stop_demon(self):
		self.arp_demon.stop()
		
	def setTargetHost(self,ipaddr):
		self.log.info('Target host: %s'%ipaddr)
		self.targethost_ip   = ipaddr
		ip.DEFAULT_TARGET_ADDR = ipaddr
		
	def getTargetHost(self):
		return (self.targethost_ip, self.targethost_mac)
	
	def getVirtualHost(self):
		return (self.virtualhost_ip, self.virtualhost_mac)

	def set_userland_socket(self, bool):
		if bool==False:
			tcp.TCPSocket.DEFAULT_SOCKET = tcp.PythonTCPSocket
		else:
			tcp.TCPSocket.DEFAULT_SOCKET = tcp.UserSpaceTCPSocket

	def is_userland_socket_enabled(self):
		if tcp.TCPSocket.DEFAULT_SOCKET == tcp.PythonTCPSocket:
			return False
		else:
			return True

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Exploit
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def load_exploit(self, filename):
		loaded = False
		try:
			if self.exp_module != None:
				del sys.modules[self.exp_module.__name__]
			directory, f = os.path.split(filename)
			sys.path.append(directory)
			if f[-3:]=='.py':
				self.exp_module  = __import__(f[:-3]) 
			elif f[-4:]=='.pyc':
				self.exp_module  = __import__(f[:-4])
			else:
				self.log.warning('Bad file name %s'%filename)
			content = dir(self.exp_module)
			for x in content:
				try:
					obj = self.exp_module.__dict__[x]
					if issubclass(obj, interfaces.exploit.Exploit):
						self.exploit = obj()
						loaded = True
						self.log.info('%s exploit loaded'%filename)
						break
				except Exception, msg: 
					#print "Error loading exploit file %s:\r\n%s"%(filename,msg)
					#junk1, junk2, trace = sys.exc_info()
					#print "Line number: %d"%trace.tb_lineno
					pass
					
					
			sys.path.remove(directory)
		except Exception, msg:
			self.log.error("Error loading exploit file %s:\r\n%s"%(filename,msg))	
		if loaded==False:
			self.exploit    = None
			self.exp_module = None

	def _apply_operators(self, oplist):
		for op in oplist:
			op.insert()

	def _remove_operators(self, oplist):
		for op in oplist:
			op.remove()

	def execute(self, number, startfrom, sleep=0,  callback=None):
		if number==0:
			self.log.info("Starting exploit execution of (all mutants from %d)"%(startfrom))
		else:
			self.log.info("Starting exploit execution of (mutants from %d to %d)"%(startfrom, number+startfrom))
		
		if self.is_userland_socket_enabled():
			 self.start_demon()
	
		# Reset the factory just in case the mutant operators list changed
		self.factory.reset()
		
		# Setup the factory to the first mutant
		if self.factory.set_first(startfrom)==False:
			self.log.info("Mutant number %d out of range"%startfrom)
			return
		

		# Setup the exploit
		self.exploit.set_up()
		
		# da rimuovere
		for c in self.collectors:
			c.connect()
			c.reset()
		explist = []
		
		next  = {}   # Mutant operators for the next mutant
		count = 0    # Number of mutant executed so far
		attempt = 0  # Number of time the service appered down


		while(count < number or number==0):
			# info will contain the exploit execution info
			info = ExecInfo()
			info.number = count
			
			# Redirect the logs to a memory buffer
			if self.redirect:
				logger.main.redirect(info.messages)
			
			self.log.info("Setting up mutant # %d"%count)
			# Ask the factory to select the operators for the next mutant
			next = self.factory.next(info)
			if next == None:
				self.log.info("No other mutant to be executed")
				break
			self.log.debug("%d mutant operators selected"%len(next))
			
			# Apply the list of mutant operators
			self._apply_operators(next)
			
			info.operators = next
			
			# Execute all the exploit-level mutant operators
			for op in DEFAULT_EXPLOIT_OPERATORS:
				op.mutate(self.exploit)
				
			try:
				info.result = interfaces.exploit.RES_ERROR # just to enter into the while loop

				self.log.info("Starting mutant execution (attempt %d)"%attempt)
				# Set the execution date/time
				info.date = time.strftime("%a, %d %b %Y %H:%M:%S",time.gmtime())
				
				# Save the TCP port at the beginning
				tcp_start_port = tcp.NEXT_SPORT
				
				# Start the timer
				timer = time.time()
				
				# And execute the exploit
				while (attempt < 3):
					try:
						self.exploit.execute()
						break
					# If the exploit report that the service is down
					except interfaces.exploit.ServiceDown:
						self.log.warning("Ouch! The service seems to be down")
						# Increase the attempt counter and sleep for a while
						attempt += 1
						time.sleep(3*attempt)
				
				# Stop the timer
				info.exectime = time.time()-timer
				
				# Save the TCP port at the end
				tcp_end_port = tcp.NEXT_SPORT
				
				# Save the tcp ports in the execution info object
				if tcp_end_port > tcp_start_port:
					info.tcp_ports[0] = tcp_start_port
					info.tcp_ports[1] = tcp_end_port - 1
					
				
				self.log.info("Mutant execution terminated\r\nStarting oracle interrogation...")
				
				# Ask the exploit the attack result
				info.result = self.exploit.isSuccessful()
				
				self.log.info("Oracle result %s"%info.result)
				
				attempt = 0
			
			except Exception, msg:
				info.result = interfaces.exploit.RES_ERROR
				self.log.warning("Exploit error: %s"%msg)
			
			# Redirect the logs to the standard error
			logger.main.redirect(sys.stderr)
			
			# Unselect the mutant operator
			self._remove_operators(next)
			
			# If the alerts must be synchrounosly collected... 
			if self.collect_sync:
				for c in self.collectors:
					c.correlate([info])
			else:
				# ... otherwise save the execution info for later
				explist.append(info)
			
			# Call the callback function
			if callback!=None and callback(count+startfrom, info) == False:
				self.log.info("Execution stopped")
				break
		
			# Check if the execution has been interrupted
			if attempt > 2:
				self.log.error("Too many attempts. Please restart the target service")
				break
					
			# Time to sleep
			if sleep > 0:
				time.sleep(sleep)
			count += 1
			
		# Good job. Now we teardown the exploit 
		self.exploit.tear_down()
		
		# If the alerts collection is asynchronous 
		if self.collect_sync == False:
			for c in self.collectors:
				c.correlate(explist)
		
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Configuration Files
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
	def load_configuration(self, filename):
		count = 0
		cmd   = None
		value = None
		userland = False
		self.log.info("Loading configuration from file %s"%filename)
			
		c = None
		
		try:
			c = CParser(filename)
		except Exception, msg:
			self.log.warning('Error: %s '%msg)
			return False
		
		# Load the exploit
		val = c.get("Exploit","script")
		if val is None:
			self.log.error("Config file does not contain any exploit script name")
			return False
		
		self.load_exploit(val)
		if self.exploit == None:
			self.log.error("Error loading exploit script: %s"%val)
			return False
		
		# Set up the parameters
		val = c.get("Exploit","parameters")
		if val is not None:
			for line in val:
				cmd,val = line.split("=",1);
				cmd = cmd.strip()
				try:
					self.exploit.set_parameter_value(cmd, eval(val))
				except Exception,e:
					self.log.error("Invalid exploit parameter %s:\n %s"%(line,e))
		
		#Network settings
		net = c.items("Network")
		ustack = c.get("Network","userland_stack").lower()
		if ustack is not None:
			res = {"ok":True, "yes": True, "1": True, "true": True, "on": True,
				   "no": False, "0": False, "false": False, "off": False}
			if res.has_key(ustack) == False:
				self.log.error("Invalid userland_stack value: %s"%ustack)
				return False
			ustack = res[ustack]	
		
		if ustack == True:
			if os.getuid() != 0:
				self.log.error("Using the userland TCP/IP stack requires root privileges")
				return False
			userland = True
			tmac = None
			sip  = None
			smac = None
		
		val = c.get("Network","iface")
		if val != None:
				self.set_iface(val)
			
		val = c.get("Network","target")
		if val is None:
			self.log.error("Section Network must contain a target item")
			return false
					
		for line in val:
			cmd,value = line.split("=",1);
			cmd = cmd.strip()
			if cmd == "ip":
				self.setTargetHost(value.strip())
			elif cmd == "mac":
				tmac = value.strip()
			else:
				self.log.warning("command %s in section %s unknown"%(cmd, "target"))
				
			
		val = c.get("Network","source")
		if val is not None:
			for line in val:
				cmd,value = line.split("=",1);
				cmd = cmd.strip()
				if cmd == "ip":
					sip = value.strip()
				elif cmd == "mac":
					smac = value.strip()
				else:
					self.log.warning("command %s in section %s unknown"%(cmd, "source"))

		if userland == True:
			if tmac == None:
				self.log.error("Target MAC missing with Userland stack enabled!!")
			if sip == None:
				self.log.error("Source IP missing with Userland stack enabled!!")
			if smac == None:
				self.log.error("Source MAC missing with Userland stack enabled!!")
			else:
				self.setVirtualHost(tmac, smac, sip)
				self.set_userland_socket(True)

		val = c.get("Network","iface")
		if val is not None:
			self.set_iface(val)

		# Factory settings
		val = c.get("Factory","script")
		if val is not None:	
			self.set_factory(utils.load_factory(val))
		
		# Mutant operators
		ops = c.items("Operators").items()
		for name, val in ops:
			op = self.opmanager.get_operator_by_name(name)
			if op == None:
				self.log.warning("Operator %s not found"%name)
				continue
			if type(value) == list:
				for line in val:
					cmd,value = line.split("=",1);
					cmd = cmd.split()
					value = value.split()
				
					pos = 0
					single_value = ''
					multi_value  = ''
					if value[0] != "'":
						pos = value[1:].find(" ")
						if pos < 0:
							single_value = value
						else:
							single_value = value[0:pos]
							multi_value  = value[pos+1:]
					else:
						while True:
							#print "searching in %s"%value[pos+1:]
							pos = value[pos+1:].find("'")
							if pos == -1:
								self.log.error("Invalid parameter value at line %d:\r\n%s"%(count, line))
								return False
							#print "found at %d"%pos
							if value[pos] != "\\":
								break
						single_value = value[0:pos+2]
						multi_value  = value[pos+2:]
					try:
						op.set_parameter_value(param, eval(single_value))
						multi_value = multi_value.strip()
						if len(multi_value) > 0 and multi_value[0] == '[':
							op.set_multiple_values(param, eval(multi_value))
					except Exception, msg:
						self.log.error("Invalid parameter value:\r\n %s"%line)
						return False
			self.opmanager.select_operator(op)
		return True
		
	def save_configuration(self, filename):
		try:
			f = open(filename,"w")
		except:
			return 
		f.write("##################################\r\n")
		f.write('#   Exploit Configuration File   #\r\n')
		f.write("##################################\r\n")
		f.write('\r\n')
		if self.exploit != None:
			f.write('[Exploit]\r\n')
			f.write('\tscript = %s\r\n'%sys.modules[self.exploit.__module__].__file__)
			pars = self.exploit.get_parameters_names()
			if len(pars) > 0:
				f.write('\tparameters = {\r\n')
				for par in pars:
					f.write('\t\t%s = %r\r\n'%(par,self.exploit.get_parameter_value(par)))
				f.write('\t}\r\n')
			f.write('\r\n')
		f.write('[Network]\r\n')
		f.write('\tiface = %s\r\n'%self.get_iface())
		f.write('\tuserland_stack = %s\r\n'%self.is_userland_socket_enabled())
		f.write('\ttarget = {\r\n')
		if self.targethost_ip != "undefined":
			f.write('\t\tip  = %s\r\n'%self.targethost_ip)
		else:	
			f.write('\t\t#ip  = %s\r\n'%self.targethost_ip)
		if self.targethost_mac == 'undefined':
			f.write('\t\t#mac = %s\r\n'%self.targethost_mac)
		else:
			f.write('\t\tmac = %s\r\n'%self.targethost_mac)
		f.write('\t}\r\n')
		f.write('\tsource = {\r\n')
		if self.virtualhost_ip == 'undefined':
			f.write('\t\t#ip = %s\r\n'%self.virtualhost_ip)
		else:
			f.write('\t\tip = %s\r\n'%self.virtualhost_ip)
		if self.virtualhost_mac == 'undefined':
			f.write('\t\t#mac = %s\r\n'%self.virtualhost_mac)
		else:
			f.write('\t\tmac = %s\r\n'%self.virtualhost_mac)
		f.write('\t}\r\n')
		
		f.write('\r\n')
		f.write('[Factory]\r\n')
		temp = sys.modules[self.factory.__module__].__file__
		f.write('\tscript = %s\r\n'%temp)
		f.write('\r\n')
		f.write('[Operators]\r\n')
		for gname, glist in self.opmanager.get_operators().iteritems():
			f.write('\r\n#  ---- %s ----\r\n'%gname)
			for op in glist:
				if op[1] == True:
					params = op[0].get_parameters_names()
					if len(params) == 0:
						f.write('\t%s\r\n'%op[0].name)
					else:
						f.write('\t%s = {\r\n'%op[0].name)
						for par in params:
							p = op[0].get_parameter(par)
							f.write('\t\t%s = %r'%(par, p.value))
							if p.is_multi_values():
						 		multi = p.get_multiple_values()
						 		if len(multi) > 0:
									 f.write("  %s"%multi)
							f.write('\r\n')
						f.write('\t}\r\n')
				else:
					f.write('#\t%s\r\n'%op[0].name)
		f.close()

