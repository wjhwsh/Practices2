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
# $Id: FTP-CmdChangeCase.py 109 2006-02-27 20:17:42Z balzarot $

import string
from FTPLayerOperator import FTPLayerOperator

class FTPCmdChangeCase(FTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		FTPLayerOperator.__init__(self,'FTPCmd-ChangeCase', 'Change the case of the ftp command')	
				
	def mutate(self, cmds):
		result = []
		for c in cmds:
			c.cmd = self.changecase(c.cmd)
			result.append(c)
		return result
		

	def changecase(self, s):
		result = ""
		ff = False
		for c in s:
			if ff:
				ff = False
				result += c
			else:
				ff = True
				result += string.swapcase(c)
		return result