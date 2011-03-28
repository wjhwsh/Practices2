"""
	Configuration file parser.
	This file is a modified version of the standard ConfigParser

"""

# Author: Davide Balzarotti
# $Id: cparser.py 34 2005-10-06 07:59:16Z balzarot $

class Error(Exception):
	"""Base class for ConfigParser exceptions."""
	def __init__(self, msg=''):
		self.message = msg
		Exception.__init__(self, msg)
	def __repr__(self):
		return self.message
	__str__ = __repr__

class ParserError(Error):
	"""Raised when a section is multiply-created."""
	def __init__(self, lineno, line):
		Error.__init__(self, "Parsing Error\n[line %d]: %s"%(lineno,line))

class CParser:
	def __init__(self, filename):
		self._sections = {}
		f = open(filename)
		self.parsefile(f)
		f.close()

	def __getattr__(self, attr):
		try:
			return self._sections[attr]
		except KeyError:
			raise AttributeError, attr
	
	def get(self, section, item):
		if self._sections.has_key(section) == False:
			return None
		if self._sections[section].has_key(item) == False:
			return None
		return self._sections[section][item]
	
	def sections(self):
		"""Return the list of section names"""
		return self._sections.keys()

	def has_section(self, section):
		"""Indicate whether the section is present or not"""
		return section in self._sections

	def items(self, section):
		if self._sections.has_key(section) == False:
			return None
		else:
			return self._sections[section]

	def remove_section(self, section):
		"""Remove a file section."""
		if self._sections.has_key(section):
			del self._sections[section]
			return True
		return False

	def parsefile(self, fp):
		currentsection = None                 # None, or a dictionary
		multiline      = None
		name = None
		value = None
		n = 0
		
		while True:
			line = fp.readline()
			n += 1
			if not line:
				break
			line = line.strip()
			if line == '' or line[0] in '#;':
				continue
			
			# multiline
			if multiline is not None:
				if line =="}":
					currentsection[name] = multiline
					multiline = None
				else:
					multiline.append(line)
				continue

			# is it a section header?
			if line[0] == "[" and line[-1] == "]":
				sectionname = line[1:-1]
				if sectionname in self._sections:
					currentsection = self._sections[sectionname]
				else:
					self._sections[sectionname] = {}
					currentsection=self._sections[sectionname]
				continue
			
			if currentsection != None:
				comma = line.find(":")
				equal = line.find("=")
				if comma==-1 and equal==-1:
					 currentsection[line] = True
					 continue
				if comma == -1:
					first = equal
				elif equal == -1:
					first = comma
				else:
					first = min(comma,equal)
				 
				name = line[:first].strip()
				value= line[first+1:].strip()
				
				if value[0] == "{":
					if value[-1] == "}":
						value = value[1:-1]
					elif len(value) == 1:
						multiline = []
						continue
				
				currentsection[name] = value
			else:
				raise ParserError(n, line)
				

