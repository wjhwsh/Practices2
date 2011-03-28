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
# $Id: hasparameters.py 130 2006-05-03 15:33:04Z balzarot $

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                           EXCEPTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class InvalidValue(Exception):
	"""Raised when one try to set an option to some invalid value"""
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return str(self.msg)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                            PARAMETERS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Parameter:
	def __init__(self, name, default, desc, isMultiValues = False):
		self.value               = self.validate(default)
		self.default             = self.validate(default)
		self.description         = desc
		self.name                = name
		self.enable_multi_values = isMultiValues
		self.multiple_values     = []
	
	def validate(self, value):
		return value
	
	def is_multi_values(self):
		return self.enable_multi_values
	
	def set_value(self, value):
		self.value = self.validate(value)
		
	def get_value(self):
		return self.value
		
	def reset(self):
		self.value = self.default

	def set_multiple_values(self, values):
		if self.enable_multi_values == False:
			return
		temp = []
		for v in values:
			temp.append(self.validate(v))
		self.multiple_values = temp

	def get_multiple_values(self):
		if self.enable_multi_values == False:
			return None
		else:
			return self.multiple_values

class StringParam(Parameter):
	def validate(self, value):
		return str(value)

class IntParam(Parameter):
	def __init__(self, name, default, desc, min=None, max=None, isMultiValues = False):
		self.min = min
		self.max = max
		Parameter.__init__(self, name, default, desc, isMultiValues)
		
	def validate(self, value):
		try:
			temp=int(value)
		except:
			raise InvalidValue("Ths value must be an Integer number")
		if (self.min != None) and (temp < self.min):
			raise InvalidValue("The parameter value must be greater than %d"%self.min)
		if (self.max != None) and (temp > self.max):
			raise InvalidValue("The parameter value must be less than %d"%self.max)
		return temp
		
class KeyListParam(Parameter):
	def __init__(self, name, default, keys, desc, isMultiValues = False):
		self.keys = keys
		Parameter.__init__(self, name, default, desc, isMultiValues)
		
	def validate(self, value):
		if (value in self.keys) == False:
			raise InvalidValue("The parameter value must one of:\r\n%s"%self.keys)
		return value

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                    INTERFACE TO PROVIDE PARAMETERS TO CLASSES 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HasParameters:	
	params     = {}
	
	def __init__(self):
		self.params = {}
	
	def __getattr__(self, attr):
		try:
			return self.params[attr].value
		except KeyError:
			raise AttributeError, attr
		
	def __setattr__(self, attr, val):
		if self.params.has_key(attr):
			fld = self.params.get(attr)
			fld.set_value(val)
		else:
			self.__dict__[attr] = val
			
	def __delattr__(self, attr):
		if self.params.has_key(attr):
			fld = self.params.get(attr)
			fld.reset()
			return
		if self.__dict__.has_key(attr):
			del(self.__dict__[attr])
		else:
			raise AttributeError(attr)	
			
	def add_param(self, param):
		self.params[param.name]=param

	def set_multiple_values(self, name, values):
		try:
			return self.params[name].set_multiple_values(values)
		except KeyError:
			msg = "Parameter <%s> does not exist"%name
			raise AttributeError, msg

	def get_multiple_values(self, name):
		try:
			return self.params[name].get_multiple_values()
		except KeyError:
			msg = "Parameter <%s> does not exist"%name
			raise AttributeError, msg
		
	def get_parameters_names(self):
		return self.params.keys()
	
	def get_parameter_value(self, name):
		try:
			return self.params[name].value
		except KeyError:
			msg = "Parameter <%s> does not exist"%name
			raise AttributeError, msg
	
	def get_parameter(self, name):
		try:
			return self.params[name]
		except KeyError:
			msg = "Parameter <%s> does not exist"%name
			raise AttributeError, msg

	def get_parameters(self):
		return self.params.values()
			
	def set_parameter_value(self, name, value):
		try:
			return self.params[name].set_value(value)
		except KeyError:
			msg = "Parameter <%s> does not exist"%name
			raise AttributeError, msg
	
	def reset_parameter_value(self, name):
		try:
			return self.params[name].reset()
		except KeyError:
			msg = "Parameter <%s> does not exist"%name
			raise AttributeError, msg
	
	def params_combinations(self):
		res = 1
		for x in self.params.values():
			if x.is_multi_values():
				n = len(x.get_multiple_values())
				if n > 0:
					res *= n
		return res

	def set_params_combination(self, n):
		tot = self.params_combinations()
		if (n >= tot) or (n < (tot*-1)):
			raise IndexError, "Combination %d out fo range"%n
		if n < 0:
			n += tot
		
		for x in self.params.values():
			if x.is_multi_values()==False:
				continue
			temp = x.get_multiple_values() 
			if len(temp) == 0: 
				continue
			which = n % len(temp)
			x.set_value(temp[which])
			n = n / len(temp)
				
