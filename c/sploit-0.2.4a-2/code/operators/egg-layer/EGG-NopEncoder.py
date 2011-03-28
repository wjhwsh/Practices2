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
# $Id: EGG-NopEncoder.py 109 2006-02-27 20:17:42Z balzarot $

import string, random
from EGGLayerOperator import EggLayerOperator

ia32_nops = ["\x50",   # push %eax  "P" 
             "\x51",   # push %ecx  "Q"
             "\x52",   # push %edx  "R"
             "\x53",   # push %ebx  "S" 
             "\x54",   # push %dsp  "T" 
             "\x55",   # push %ebp  "U" 
             "\x56",   # push %esi  "V" 
             "\x57",   # push %edi  "W" 
             "\x58",   # pop %eax   "X" 
             "\x59",   # pop %ecx   "Y"
             "\x5a",   # pop %edx   "Z"
             "\x5b",   # pop %ebx   "[" 
             "\x5d",   # pop %ebp   "]" 
             "\x5e",   # pop %esi   "^" 
             "\x5f",   # pop %edi   "_" 
             "\x60",   # pusha      "`" 
             "\x9b",   # fwait          
             "\x9c",   # pushf          
             "\x9e",   # safh
             # dangerous opcodes section over
             "\x99",   # cltd           
             "\x96",   # xchg %eax,%esi 
             "\x97",   # xchg %eax,%edi 
             "\x95",   # xchg %eax,%ebp 
             "\x93",   # xchg %eax,%ebx 
             "\x91",   # xchg %eax,%ecx 
             "\x90",   # regular NOP    
             "\x4d",   # dec %ebp,  "M" 
             "\x48",   # dec %eax,  "H" 
             "\x47",   # inc %edi   "G"
             "\x4f",   # dec %edi   "O" 
             "\x40",   # inc %eax   "@" 
             "\x41",   # inc %ecx   "A" 
             "\x37",   # aaa        "7" 
             "\x3f",   # aas        "?" 
             "\x97",   # xchg %eax,%edi 
             "\x46",   # inc %esi   "F" 
             "\x4e",   # dec %esi   "N" 
             "\xf8",   # clc            
             "\x92",   # xchg %eax,%edx 
             "\xfc",   # cld            
             "\x98",   # cwtl           
             "\x27",   # daa        "'" 
             "\x2f",   # das        "/" 
             "\x9f",   # lahf           
             "\xf9",   # stc            
             "\x4a",   # dec %edx   "J" 
             "\x44",   # inc %esp   "D" 
             "\x42",   # inc %edx   "B" 
             "\x43",   # inc %ebx   "C" 
             "\x49",   # dec %ecx   "I" 
             "\x4b",   # dec %ebx   "K" 
             "\xf5",   # cmc            
             "\x45",   # inc %ebp   "E" 
             "\x4c"]   # dec %esp   "L"

ia32_danger  = ["\x50","\x51","\x52","\x53","\x54","\x55","\x56",
                "\x57","\x58","\x59","\x5a","\x5b","\x5d","\x5e",
                "\x5f","\x60","\x9b","\x9c","\x9e"]
ia32_letters = ["\x50","\x51","\x52","\x53","\x54","\x55","\x56",
                "\x57","\x58","\x59","\x5a","\x4d","\x48","\x47",
                "\x4f","\x41","\x46","\x4e","\x4a","\x44","\x42",
                "\x43","\x49","\x4b","\x45","\x4c"]
ia32_alpha = ia32_letters + ["\x27","\x2f","\x37","\x3f","\x40",
                            "\x5b","\x5d","\x5e","\x5f","\x60"]

class EggNopEncoder(EggLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		EggLayerOperator.__init__(self,'Nop-Encoder', 'Obfuscate the nop sled')	
				
	def mutate(self, egg):
		charset = None
		if egg.only_alpha:
			charset = [e for e in ia32_alpha]
		else:
			charset = [e for e in ia32_nops]
			
		if egg.danger == False:
			for c in ia32_danger:
				charset.remove(c)

		if egg.icase:
			for c in ia32_letters:
				charset.remove(c)
				
		for c in egg.exclude:
			charset.remove(c)
		
		result = []
		for n in xrange(len(egg.nopsled)):
			result.append(random.choice(charset))
		egg.nopsled = string.join(result,"")
		return egg

