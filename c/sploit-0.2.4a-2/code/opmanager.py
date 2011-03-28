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
# $Id: opmanager.py 107 2006-02-27 19:34:25Z balzarot $

import os, sys, os.path
import time

import logger
from interfaces.mutant_operator import MutantOperator

class OperatorNotFound(Exception):
	""" Raised any time a given operator is not found"""
	
	def __init__(self, name=''):
		self.message = name
		Exception.__init__(self, name)
	def __repr__(self):
		return self.message
	__str__ = __repr__


def _my_import(name):
	mod = __import__(name)
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod

class OpManager:
	
	def __init__(self):
		# list of all the available mutant operators
		self.oplist 	   = {}
		self.log           = logger.main.newSource("OP-MANAGER")

	def load_operators(self):
		self.oplist = {}
		num = 0
		import operators
		for p_name in operators.__all__:
			#print "Package %s"%p_name
			packages = _my_import("operators.%s"%p_name)
			for mod_name in packages.__all__:
				mod = _my_import("operators.%s.%s"%(p_name, mod_name))
				content = dir(mod)
				for x in content:
					if x[0] == "_":
						continue
					try:
						obj = mod.__dict__[x]
						if issubclass(obj,MutantOperator):
							if obj.isa_operator:
								try:
									temp = obj()
									#print " - Loaded: %s"%temp.name
								except Exception, msg:
									self.log.error("ERROR loading operator %s: %s"%(obj,msg))
									continue
								if self.get_operator_by_name(temp.name)!=None:
									self.log.warning("I've found two different mutant operator with the same name: %s"%temp.name)
									continue
								num += 1
								if self.oplist.has_key(temp.group):
									self.oplist[temp.group].append([temp, False])
								else:
									self.oplist[temp.group]=[[temp, False]]
					except Exception, msg:
						pass
		self.log.info('%d mutant operators loaded'%num)				


	def get_operator_by_name(self, name):
		for gname, glist in self.oplist.iteritems():
			for op in glist:
				if str(op[0].name) == name:
					return op[0]

	def is_selected(self, op):
		for gname, glist in self.oplist.iteritems():
			for obj, sel in glist:
				if ((type(op) is str ) and (str(obj.name) == op)) or obj == op:
					return sel
		raise OperatorNotFound, op
						
	def move_up(self, op):
		if self.oplist.has_key(op.group):
			l = self.oplist[op.group]
		else:
			raise OperatorNotFound, op.__class__
		
		i = 0
		for tmp, sel in l:
			if tmp == op:
				break
			i += 1
		
		if i == len(l):
			raise OperatorNotFound, op.__class__
		elif i < 1:
			return
		
		res = l[:i-1]
		res.append(l[i])
		res.append(l[i-1])
		self.oplist[op.group] = res+l[i+1:]
		
	def move_down(self, op):
		if self.oplist.has_key(op.group):
			l = self.oplist[op.group]
		else:
			raise OperatorNotFound, op.name
		
		i = 0
		for tmp, sel in l:
			if tmp == op:
				break
			i += 1
		
		if i == len(l):
			raise OperatorNotFound, op.name
		elif i == len(l)-1:
			return
		
		res = l[:i-1]
		res.append(l[i+1])
		res.append(l[i])
		self.oplist[op.group] = res+l[i+2:]

	def _set_selection(self,op,val):
		if self.oplist.has_key(op.group):
			l = self.oplist[op.group]
		else:
			raise OperatorNotFound, op.name
		
		for tmp in l:
			if tmp[0] == op:
				tmp[1] = val
				return
		raise OperatorNotFound(op.name)
					
	def unselect_operator(self, op):
		self._set_selection(op, False)
							
	def select_operator(self, op):
		self._set_selection(op, True)
							
	def get_selected_operators(self):
		result = []
		for group in self.oplist.values():
			for op, sel in group:
				if sel == True:
					result.append(op)
		return result
	
	def get_operators(self):
		return self.oplist


if __name__ == "__main__":
	om = OpManager()
	om.load_operators()
	for group, names in om.oplist.items():
		print group
		for n,junk in names:
			print " - %s"%n.name
