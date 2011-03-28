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
# $Id$

from interfaces.mutant_operator import MutantOperator
import managers.tcp as tcp

class TCPLayerOperator(MutantOperator):	
	
	group             = 'TCP Layer' 
	group_description = '''This mutations are applied to the TCP packets before sending them to the target'''
	isa_operator      = False  # cannot be instanciated

#	def __init__(self, name, desc):
#		MutantOperator.__init__(self, name, desc)		
	
	def mutate(self, packets):
		return packets
		
	def insert(self):
		tcp.DEFAULT_TCP_OPERATORS.append(self)
	
	def remove(self):
		tcp.DEFAULT_TCP_OPERATORS.remove(self)
