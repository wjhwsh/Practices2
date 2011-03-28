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
# $Id: execinfo.py 107 2006-02-27 19:34:25Z balzarot $

# Python import
import sys, string
from time import gmtime, strftime
import interfaces.exploit

class StringListOutput:
	"""
	During the execution of a mutant the standard error is redirected here
	"""
		
	def __init__(self):
		self.strings = []
	
	def write(self, text):
		self.strings.append(text); 
	
	def getText(self):
		return string.join(self.strings)

	def clear(self):
		self.strings = []

class ExecInfo:
	"""
	Used to memorize all the details of a mutant execution
	"""
	
	def __init__(self):
		self.number     = None
		self.messages   = StringListOutput()
		self.operators  = []
		self.tcp_ports  = [0,0]
		self.udp_ports  = [0,0]
		self.result     = interfaces.exploit.RES_UNKNOWN
		self.exectime   = 0
		self.date       = ""
		
	def write_to_file(self, filename):
		f = open(filename,"w")
		f.write("Mutant #%d\r\n"%self.number)
		if self.tcp_ports[1] != 0:
			if self.tcp_ports[0] == self.tcp_ports[1]: 
				f.write("TCP Port: %d\r\n"%self.tcp_ports[0])
			else:
				f.write("TCP Ports: %d:%d\r\n"%(self.tcp_ports[0],self.tcp_ports[1]))
		if self.udp_ports[1] != 0:
			if self.udp_ports[0] == self.udp_ports[1]: 
				f.write("UDP Port: %d\r\n"%self.udp_ports[0])
			else:
				f.write("UDP Ports: %d:%d\r\n"%(self.udp_ports[0],self.udp_ports[1]))
		f.write("Execution Date: %s\r\n"%self.date)
		f.write("Execution Time: %d\r\n"%self.exectime)
		f.write("Attack Result: %d\r\n"%self.result)
		f.write("-------------------[ Mutant Operators ]--------------------\r\n")
		for o in self.operators:
			f.write("o %s\r\n"%o.name)
			if len(o.get_parameters()) == 0:
				continue
			for p in o.get_parameters():
				f.write("    %s = %r\r\n"%(p.name,p.value))
		f.write("----------------------[ Log Messages ]----------------------\r\n")
		for l in self.messages.getText():
			f.write(l)
		f.close()
	

	
	
