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
# $Id: IPLayerOperator.py 66 2005-11-17 12:03:14Z balzarot $


from interfaces.mutant_operator import MutantOperator
import managers.ip as ip
 
class IPLayerOperator(MutantOperator):	
	
	group             = 'IP Layer' 
	group_description = '''This mutations are applyed to the IP packets before sending them to the target'''
	isa_operator      = False  # cannot be instanciated

	def mutate(self, packets):
		return packets
		
	def insert(self):
		ip.DEFAULT_IP_OPERATORS.append(self)
	
	def remove(self):
		ip.DEFAULT_IP_OPERATORS.remove(self)
