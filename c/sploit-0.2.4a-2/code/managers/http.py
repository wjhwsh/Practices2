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
# $Id: http.py 109 2006-02-27 20:17:42Z balzarot $

import string

import tcp
import logger

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         DEFAULT VALUES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DEFAULT_HTTP_OPERATORS = []
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HttpResponse:
	def __init__(self, version, status, reason, header, data=None):
		self.version = version
		self.status  = status
		self.reason  = reason
		self.data    = data
		self.header  = header

	def setHeaderValue(self, name, value):
		self.header[name.upper()] = value
	
	def getHeaderValue(self, name):
		return self.header[name.upper()]

	def hasKey(self, name):
		return self.header.has_key(name.upper())

	def __str__(self):
		if self.version == '0.9':
			return "HTTP 0.9 Simple Response:\r\n"+self.data
		else:
			result = "%s %s %s\r\n"%(self.version, self.status, self.reason)
			header = ''
			for name,value in self.header.iteritems():
				header = header + name + ": "+ value + "\r\n"
			if self.data == None:
				return result + header 
			else:
				return result + header +"\r\n"+self.data

class Chunk:
	def __init__(self, data, size = None):
		self.data = data
		if size:
			if type(size) == int:
				self.size = "%x"%size
			else:
				self.size = str(size)
		else:
			self.size = "%x"%len(self.data)
		self.before_size = ''
		self.size2ext    = ''
		self.extension   = ""
		self.ext2data    = '\r\n'
		self.afterdata   = '\r\n'
	
	def __str__(self):
		return "%s%s%s%s%s%s%s"%(self.before_size, self.size, self.size2ext, self.extension, self.ext2data, self.data, self.afterdata)


# TODO: add support for trailer after the last chunk
class ChunkList:
	# addfinal: True means that the ChunkList will be automatically terminated
	# with a zero length chunk
	def __init__(self, addfinal = True):
		self.clist = []
		self.addfinal = addfinal
		self.last = Chunk("")

	def add(self, chunk):
		self.clist.append(chunk)
	
	def __str__(self):
		res = str(self.clist[0])
		for x in self.clist[1:]:
			res += str(x)
		res += str(self.last)
		return res


class HttpRequest:
	def __init__(self, request, header={}, data=None ):
		request = request.strip()
		r = request.split()
		
		self.url     = r[1]
		self.params  = ''
		pos = self.url.find('?')
		if pos>0:
			self.params  = self.url[pos:]
			self.url = self.url[:pos]
			
		self.method  = r[0].upper()
		
		if len(r) == 3:
			self.version = r[2][5:]
		else:
			self.version = "1.1"
		
		self.header  = {}
		for key,value in header.iteritems():
			self.header[key.upper()]=value
		
		self.data    = data
		
		self.before_method    = ''
		self.method2url       = ' '
		self.url2version      = ' '
		self.http             = 'HTTP'
		self.http2version     = '/'
		self.version2header   = '\r\n'
		self.header_separator = ':'
		self.header_eol       = '\r\n'
		self.after_header     = '\r\n'
		
	def __str__(self):
		result = "%s%s%s%s%s%s%s%s%s%s"%(self.before_method, self.method, self.method2url, self.url,self.params, self.url2version, self.http, self.http2version, self.version, self.version2header)
		header = ''
		for name,value in self.header.iteritems():
			header = header + name + self.header_separator + value + self.header_eol
		if self.data == None:
			return result + header + self.after_header
		else:
			return result + header + self.after_header + str(self.data)
	
	def setHeaderValue(self, name, value):
		self.header[name.upper()] = value
	
	def getHeaderValue(self, name):
		return self.header[name.upper()]

	def hasKey(self, name):
		return self.header.has_key(name.upper())
	
class HttpManager:
	''' Manages HTTP connection with polymorphic command '''
	
	def __init__(self, port=80):
		self.port    = port
		self.sock    = tcp.TCPSocket()
		self.log     = logger.main.newSource("HTTP")
		self.filters = DEFAULT_HTTP_OPERATORS

	def send_raw(self, data):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False

		self.log.debug("Sending %d byte of raw data"%len(data))
		
		self.sock.send(str(data))
		return True
				
	def send_request(self, request):
		if self.sock.is_open() == False:
			self.log.info('Open Connection to port %d'%self.port)
			if self.sock.connect(dport=self.port) == False:
				self.log.error('Impossible to open a connection to the server')
				return False
			
		if type(request) is str:
			request = HttpRequest(request)
		requests = [request]
		
		self.log.info('Apply HTTP Filters')
		for mf in self.filters:
			requests = mf.mutate(requests)
		
		for r in requests:
			self.log.debug("Sending...\r\n%r"%str(r))
			try:
				self.sock.send(str(r))
			except Exception, e:
				self.log.error("Ouch, something's wrong: %s"%e)
				return False
		return True
			
	def get_raw_response(self):
		return self.sock.read(1024)
		
	def get_http_response(self, timeout = 0):
		line   = self.sock.readline('\r\n',blocking=True, timeout=5)
		line = line.strip()
				
		if line==None: 
			self.log.warning('No response from the server')
			return None
		if line[:4]!="HTTP":
			self.log.info('Simple 0.9 response from the server')
			res = HttpResponse('0.9','unknown','unknown',None)
			data = self.sock.read()
			res.data = line + data
			return res
		
		self.log.info('Response: %s'%line)
					
		try:
			version, status, reason = line.split(None, 2)
			headerdata = self.sock.readline('\r\n\r\n',blocking=True, timeout=3)
			header = {}
			key = None
			for line in headerdata.split('\r\n'):
				if line[0]==' ' or line[0]=='\t':
					header[key] += line.strip()
				else:
					key, value = line.split(':',1)
					key   = key.upper()
					value = value.strip()
					if header.has_key(key):
						header[key] += ','+value
					else:
						header[key] = value
			res = HttpResponse(version,status,reason,header)
		except:
			self.log.error("There is something wrong in the HTTP header")
			tmp = HttpResponse(version,status,reason, {})
			if headerdata != None: 
				tmp.data = headerdata
			return tmp
		
		self.log.debug('Header Received')
		
		if (status == 204 or            # No Content
			status == 304 or            # Not Modified
			100 <= status < 200):       # 1xx codes
				return res
	
		if res.hasKey('Content-Length'):
			size = int(res.getHeaderValue('Content-Length'))
			res.data = ""
			rcv = 0
			while rcv < size:
				data = self.sock.read(size, blocking=True, timeout=3)
				if data == None:
					break
				rcv += len(data)
				res.data += data
			self.log.debug('Content Received')
			
		elif res.hasKey("Transfer-Encoding"):
			res.data = ""
			chunksize = self.sock.readline('\r\n',blocking=True, timeout=3)
			size = int(chunksize.strip(),16)
			self.log.debug("First chunk size: %s"%size)
			while size > 0:
				rcv = 0
				while rcv < size:
					data = self.sock.read(size, blocking=True, timeout=3)
					if data == None:
						break
					rcv += len(data)
					# print "RCV: %d"%rcv
					res.data += data
				chunksize = self.sock.readline('\r\n',blocking=True, timeout=3)
				chunksize = self.sock.readline('\r\n',blocking=True, timeout=3)
				size = int(chunksize.strip(),16)
				self.log.debug("Next chunk size: %s"%size)
			self.log.debug('All chunks correctly received')

		return res
		
	def close(self):
		self.sock.half_close()

	#def __del__(self):
	#	self.sock.abort()

		
		
