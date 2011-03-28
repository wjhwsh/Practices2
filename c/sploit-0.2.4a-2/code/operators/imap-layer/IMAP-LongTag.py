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
# $Id: IMAP-LongTag.py 109 2006-02-27 20:17:42Z balzarot $

import string
from IMAPLayerOperator import IMAPLayerOperator
from interfaces.hasparameters import IntParam

class ImapLongTag(IMAPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IMAPLayerOperator.__init__(self,'LongTag', 'Change the case of the imap command')	
		self.add_param(IntParam('LEN',40,'Length of the tag'))
				
	def mutate(self, cmds):
		result = []
		for c in cmds:
			l = len (c.tag)
			if l < self.LEN:
				c.tag = c.tag+'x'*(self.LEN-l)
			result.append(c)
		return result
		
