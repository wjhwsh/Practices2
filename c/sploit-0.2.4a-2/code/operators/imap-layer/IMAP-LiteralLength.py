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
# $Id: IMAP-LiteralLength.py 109 2006-02-27 20:17:42Z balzarot $

import string
from IMAPLayerOperator import IMAPLayerOperator
from interfaces.hasparameters import IntParam

class ImapLiteralLength(IMAPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IMAPLayerOperator.__init__(self,'LiteralLengthObfuscator', 'Modify the number between curly braces that represents the length of a literal string')	
		self.add_param(IntParam('LEN',20,'Number of zeros in front of the number'))
				
	def mutate(self, cmds):
		for c in cmds:
			temp = []
			for p in c.parameters:
				if p[0]=='{' and p[-1]=='}':
					temp.append('{%s%s}'%('0'*self.LEN, p[1:-1]))
				else:
					temp.append(p)
			c.parameters = temp
		return cmds
		
