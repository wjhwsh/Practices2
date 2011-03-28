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
# $Id: ftp.py 109 2006-02-27 20:17:42Z balzarot $

# System import
import string

# Sploit import
import tcp
import logger

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         DEFAULT VALUES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DEFAULT_FTP_OPERATORS = []
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FTPCommand:
	def __init__(self, command, parameters=None):
		if parameters==None:
			temp = command.strip().split()
					
			command = temp[0]
			if len(temp) > 1:
				parameters = temp[1:]
			else:
				parameters = []
				
		self.cmd = command.upper()
		self.parameters = parameters
			
		self.param_separator = ' '
		self.before_cmd      = ''
		self.before_eol      = ''
		self.eol             = '\r\n'
		self.cmd2params      = ' '
				
	def __str__(self):
		return "%s%s%s%s%s%s"%(self.before_cmd, self.cmd, self.cmd2params, string.join(self.parameters,self.param_separator),self.before_eol,self.eol)
		
class FTPManager:
	''' Manages FTP connection with polymorphic command '''
	
	def __init__(self, port=21):
		self.port    = port
		self.sock    = tcp.TCPSocket()
		self.log     = logger.main.newSource("FTP")
		self.filters = DEFAULT_FTP_OPERATORS
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
				
	def connect(self):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False
			self.welcome = self.get_ftp_response()
		return True
	
	def send_cmd(self, cmd):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False
			self.welcome = self.get_ftp_response()
			
		if type(cmd) is str:
			cmd = FTPCommand(cmd)
		cmds = [cmd]
		
		self.log.debug('Applying FTP Filters')
		for mf in self.filters:
			cmds = mf.mutate(cmds)
		
		for r in cmds:
			self.log.debug("Sending...\r\n%r"%str(r))
			self.sock.send(str(r))
		return True
			
	def get_raw_response(self):
		return self.sock.read()
		
	def get_ftp_response(self):
		res = self.sock.readline('\r\n',blocking=True)
		res_strip = res.strip()
		if res_strip[3:4] == '-':
			code = res_strip[:3]
			while 1:
				nextline = self.sock.readline('\r\n',blocking=True)
				nextline_strip = nextline.strip()
				res = res + '\n' +nextline
				if nextline_strip[:3] == code and nextline_strip[3:4] == ' ': 
					break
		return res
		
	def close(self):
		self.sock.half_close()
		
