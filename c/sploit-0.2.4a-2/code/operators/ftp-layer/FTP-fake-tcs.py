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
# $Id: FTP-fake-tcs.py 109 2006-02-27 20:17:42Z balzarot $


from FTPLayerOperator import FTPLayerOperator
from interfaces.hasparameters import StringParam
import string

desc = 'Insert a fake TELNET control sequence in each command word'

complete_list = ["\xff\xf0","\xff\xf1","\xff\xf2","\xff\xf3","\xff\xf4",
				"\xff\xf5","\xff\xf6","\xff\xf7","\xff\xf8","\xff\xf9",
				"\xff\xfba","\xff\xfca","\xff\xfda","\xff\xfea",
				"\xff\xfb\xff","\xff\xfc\xff","\xff\xfd\xff","\xff\xfe\xff"]

class FTPTCS(FTPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		FTPLayerOperator.__init__(self,'Telnet-Control-Sequences', desc)	
		temp = StringParam('TCS','\xffa','Control sequence to be inserted', isMultiValues=True)
		#temp.set_multiple_values(["\xffa","\xff\xf0","\xff\xf1","\xff\xfb\xff"])
		temp.set_multiple_values(complete_list)
		self.add_param(temp)

	def insert_cc(self, s):
		if '%' in s:
			return s.replace('%','\xffa%')
		elif len(s) > 1:
			return s[0]+self.TCS+s[1:]
		else:
			return self.TCS+s
				
	def mutate(self, cmds):
		result = []
		for c in cmds:
			c.cmd = self.insert_cc(c.cmd)
			tmp = []
			for p in c.parameters:
				tmp.append(self.insert_cc(p))
			c.parameters = tmp
			result.append(c) 
		return result
		
