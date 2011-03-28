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
# $Id: FTPLayerOperator.py 109 2006-02-27 20:17:42Z balzarot $


from interfaces.mutant_operator import MutantOperator
import managers.ftp as ftp

class FTPLayerOperator(MutantOperator):
	
	group             = 'FTP Layer' 
	group_description = '''This mutations are applied to any FTP commands before sending them to the target'''
	isa_operator      = False  # cannot be instanciated
	
	def mutate(self, requests):
		return requests
		
	def insert(self):
		ftp.DEFAULT_FTP_OPERATORS.append(self)
	
	def remove(self):
		ftp.DEFAULT_FTP_OPERATORS.remove(self)

				
