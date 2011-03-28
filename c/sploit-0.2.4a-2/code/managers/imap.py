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
# $Id: imap.py 111 2006-03-01 20:29:47Z balzarot $

import string
import tcp
import logger

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         DEFAULT VALUES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DEFAULT_IMAP_OPERATORS = []
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IMAPCommand:
	tagnumber = 0
	
	def __init__(self, command, tag=None):
		temp = command.strip().split()
				
		self.cmd = temp[0].upper()
		self.parameters = []
		if len(temp) > 1:
			count = 1
			quoted = None
			while count <= len(temp[1:]):
				p = temp[count]
				if p[0]=='"' and p[-1]=='"':
					self.parameters.append(p)
					count += 1
					continue
				if quoted != None:
					if p[0]=='"' or p[-1]=='"':
						self.parameters.append(quoted+p)
						quoted = None
					else:
						quoted += p
				else:
					if p[0]!='"':
						self.parameters.append(p)
					else:
						quoted = p
				count += 1
			
		if tag != None:
			self.tag = tag
		else:
			self.tag = 'a'+str(IMAPCommand.tagnumber)
			IMAPCommand.tagnumber += 1
		self.before_tag      = ''
		self.tag2cmd         = ' '
		self.cmd2params      = ' '
		self.param_separator = ' '
		self.before_eol      = ''
		self.eol             = '\r\n'
	
	def byte_to_field(self, byte):
		n = len(self.before_tag)
		if byte < n:
			return "before_tag"
		
		n += len(self.tag)
		if byte < n:
			return "tag"
		
		n += len(self.tag2cmd)
		if byte < n:
			return "tag2cmd"
		
		n += len(self.cmd)
		if byte < n:
			return "cmd"
		
		n += len(self.cmd2params)
		if byte < n:
			return "cmd2params"
		
		n += len(self.cmd2params)
		if byte < n:
			return "cmd2params"

		if len(self.parameters) > 0:
			n += len(self.parameters[0])
			if byte < n:
				return "parameters"
			for p in self.parameters[1:]:
				n += len(self.param_separator)
				if byte < n:
					return "param_separator"
				n += len(p)
				if byte < n:
					return "parameters"
		
		n += len(self.before_eol)
		if byte < n:
			return "before_eol"
		
		n += len(self.eol)
		if byte < n:
			return "eol"

		return None
	
	def __str__(self):
		return "%s%s%s%s%s%s%s%s"%(self.before_tag, self.tag, self.tag2cmd, self.cmd, self.cmd2params, string.join(self.parameters,self.param_separator),self.before_eol,self.eol)
		
class IMAPManager:
	''' Manages IMAP connection with polymorphic command '''
	
	def __init__(self, port=143):
		self.port    = port
		self.sock    = tcp.TCPSocket()
		self.log     = logger.main.newSource("IMAP")
		self.filters = DEFAULT_IMAP_OPERATORS
		self.welcome = None
			
	def send_raw(self, data):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False
			self.welcome = self.sock.readline('\r\n',blocking=True)
		
		self.log.debug("Sending %d byte of raw data"%len(data))
		
		self.sock.send(str(data))
		return True

	def get_banner(self):
		return self.welcome

	def get_socket(self):
		return self.sock

	def connect(self):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False
			self.welcome = self.sock.readline('\r\n',blocking=True)
			self.log.info("Banner: %s"%self.welcome)
			return True
		return False
		
	def send_cmd(self, cmd):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False
			self.welcome = self.sock.readline('\r\n',blocking=True)
			self.log.info("Banner: %s"%self.welcome)
				
		if type(cmd) is str:
			cmd = IMAPCommand(cmd)
		cmds = [cmd]
		
		self.log.info('Apply Imap Filters')
		for mf in self.filters:
			cmds = mf.mutate(cmds)
		
		for r in cmds:
			self.log.debug("Sending...%s"%r)
			self.sock.send(str(r))
		return True
	
	def get_raw_response(self, tag=None):
		return self.sock.read()
		
	def get_imap_response(self):
		res = ''
		while True:
			line = self.sock.readline('\r\n',blocking=True)
			if line[0] == '+':
				res += line
				break
			if line[0] == '*':
				res += line
				continue
			try:
				rcvtag, message = line.split(' ',1)
				res += line
				break
			except:
				pass
		return res
		
	def close(self):
		try:
			self.sock.half_close()
		except:
			pass

		
		
		
		
