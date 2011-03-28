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
# $Id: IMAP-ReplaceCommand.py 109 2006-02-27 20:17:42Z balzarot $

import string
from IMAPLayerOperator import IMAPLayerOperator
from interfaces.hasparameters import StringParam


class ImapReplaceCommand(IMAPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IMAPLayerOperator.__init__(self,'IMAPReplaceCommand', 'Substitute a commmand with another')	
		self.add_param(StringParam('From','LSUB','Command to be replaced', True))
		param = StringParam('To','RENAME','Command alternatives', True)
		param.set_multiple_values(['RENAME', 'COPY', 'FIND', 'LIST'])

	        self.add_param(param)
						
	def mutate(self, cmds):
		result = []
		for c in cmds:
			if c.cmd == self.From:
				c.cmd = self.To
			result.append(c)
		return result
		
