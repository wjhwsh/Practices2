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
# $Id: EGG-clet.py 109 2006-02-27 20:17:42Z balzarot $

# IMPORTANT
# This operator requires that clet has previously been installed on the system


import os,time
from EGGLayerOperator import EggLayerOperator

class CletWrapper(EggLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		EggLayerOperator.__init__(self,'Clet-Wrapper','Clet shellcode obfuscator wrapper')
				
	def mutate(self, egg):
		original_len = len(egg.shellcode)
		f = open("/var/tmp/sploit-clet.tmp","w")
		f.write(egg.shellcode);
		f.close()
		p = os.popen("clet -S /var/tmp/sploit-clet.tmp -d > /var/tmp/sploit-clet.out")
		time.sleep(1)
		f = open("/var/tmp/sploit-clet.out","r")
		obfuscated = f.read()
		f.close()
		
		obfuscated_len = len(obfuscated)
		diff = obfuscated_len - original_len
		if len(egg.nopsled) < diff:
			printf("Impossible to obfuscate. To little space");
			return egg
		
		print "PRIMA:"
		print "nop %d"%len(egg.nopsled)
		print "code %d"%len(egg.shellcode)
		print "ret %d"%len(egg.ret)
		
		# Truncate the nop in order to mantain the same egg size
		if diff > 0:
			egg.nopsled = egg.nopsled[:-1*diff]
		egg.shellcode = obfuscated
		
		print "DOPO:"
		print "nop %d"%len(egg.nopsled)
		print "code %d"%len(egg.shellcode)
		print "ret %d"%len(egg.ret)

		return egg

