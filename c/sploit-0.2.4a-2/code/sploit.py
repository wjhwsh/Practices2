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
# $Id: sploit 111 2006-03-01 20:29:47Z balzarot $

import sys, os
import os.path
import time
import random

import utils
import engine
import logger
from optparse import OptionParser
import interfaces.exploit
from managers import tcp

# Color constant values 
RED    = 31
BLUE   = 34
GREEN  = 32
YELLOW = 33

class CLInterface:
	
	def __init__(self):
		self.use_color  = False
		self.maincolor  = BLUE
		self.to_be_exec = 0
		self.options    = None
		self.start      = 0
		self.e          = engine.Engine()
		self.exec_info  = False
		self.exec_run   = False
		self.logenable  = False
		self.callback   = None
		self.sleep_time = 0

	def color(self, s, color):
		if self.use_color:
			return "\033[%d;1m%s\033[0m"%(color,s)
		else:
			return s

	def parse_options(self, argv=None):
		parser = OptionParser(version="Sploit mutation engine version %s"%engine.VERSION, 
                      usage="%prog [options] attack-cfg")
		options = None
		parser.add_option("-r", "--run", 
			action="store", dest="run", metavar="RANGE",
			help="execute mutants in RANGE (use 'all' to execute all of them")
		parser.add_option("-i","--info",
			action="store_true", dest="info",
			help="print attack and configuration info")
		parser.add_option("-q", "--quiet", 
			action="store_true", dest="quiet",
			help="don't print any messages to stdout")
		parser.add_option("-p", "--port", 
			action="store", dest="port",
			help="set the first TCP port used to generate packets (use 'random' for random value)")
		parser.add_option("--sleep", 
			action="store", dest="sleep", type = "int", default=0,
			help="sleep time (in seconds) between mutant executions")
		parser.add_option("--noredirect", 
			action="store_false", dest="redirect", default=True,
			help="prints all the log messages on the sandard output")
		parser.add_option("--color", 
			action="store_true", dest="color", default=False,
			help="use colors")
		parser.add_option("--dest", 
			action="store", dest="dest", metavar="IP",
			help="Set the target IP")
		parser.add_option("--nolog",
			action="store_false", dest="log", default=True,
			help="Disable logging")
		parser.add_option("-L","--log",
			action="store", type="string", dest="log_path", metavar="PATH",
			default = ".", help="Change the logging directory to PATH")
		parser.add_option("-F","--factory",
			action="store", type="string", dest="factory", metavar="FILE",
			help="Load and set the mutant factory from FILE")
		parser.add_option("-C","--collector",
			action="append", type="string", dest="collectors", metavar="FILE",
			help="Load and set an alert collector")
		parser.add_option("-v","--verbosity",
			action="append", type="string", dest="verbosity", default=[],
			help="set the verbosity level (one of DEBUG, INFO, WARNING, ERROR)")
	
		(options, args) = parser.parse_args(argv)
		
		if len(args) != 1:
			parser.error("incorrect number of arguments")
		self.file  = args[0]
		
		if options.sleep:
			self.sleep_time = options.sleep
			
		if options.color == True:
			self.use_color = True
		
		for v in options.verbosity:
			table = {
				"DEBUG":   logger.DEBUG,
				"INFO":    logger.INFO,
				"WARNING": logger.WARNING,
				"ERROR":   logger.ERROR,
				"OFF":     logger.OFF
			}
			if ":" in v:
				source, level = v.split(":")
				if table.has_key(level)==False:
					parser.error("Verbosity can be set to DEBUG, INFO, WARNING, ERROR")
				if logger.main.setLevel(table[level],source) == False:
					print "Invalid source %s"%source
					
			else:
				if table.has_key(v)==False:
					parser.error("Verbosity can be set to DEBUG, INFO, WARNING, ERROR")
				if logger.main.setLevel(table[v]) == False:
					print "Error setting the log level"
		
		if options.port != None:
			if options.port=="random":
				tcp.NEXT_SPORT = random.randint(2000,60000)
				#print "Source Port Starting from: %d"%tcp.NEXT_SPORT
			else:
				tcp.NEXT_SPORT = int(options.port)
		
		if self.e.load_configuration(self.file)==False:
			print self.color("\r\nSploit: Error loading configuration file",RED)
			return False
	
		if options.factory != None:
			temp = utils.load_factory(options.factory)
			if temp == None:
				parser.error("Error reading file"%options.factory)
			self.e.set_factory(temp)
		
		if options.log and options.run and options.redirect:
			self.logenable = True
			if os.path.isdir(options.log_path) == False:
				parser.error("Path %s must be an existing directory"%options.log_path)
			newdir = time.strftime("%d-%b-%Y_%H.%M.%S")
			self.log_full = os.path.join(options.log_path,newdir)
			try:
				os.mkdir(self.log_full)
			except:
				print "Error creating %s: access denied"%self.log_full
				return False
		
		if options.dest:
			self.e.setTargetHost(options.dest)
		
		if options.collectors:
			for c in options.collectors: 
				self.e.add_collector(utils.load_collector(c))
		
		if options.info:
			self.exec_info = True
		
		if options.run:
			self.exec_run  = True
			if ":" in options.run:
				try:
					start, end = options.run.split(":")
					self.start = int(start)
					self.to_be_exec = 1 + (int(end)-self.start)
				except:
					parser.error("Execution RANGE must be a number or a windows in the form FIRST:LAST")
			else:
				if options.run == "all":
					self.start = 0
					self.to_be_exec = 0
				else:
					try:
						self.start = int(options.run)
						self.to_be_exec = 1
					except:
						parser.error("Execution RANGE must be a number or a windows in the form FIRST:LAST")
			
		if options.redirect != None and options.redirect==False:
			self.e.redirect = False
		
		return True
	
	def set_callback(self, f):
		self.callback = f
		
	def run(self):
		def local_callback(number, info):
			print "Mutant %d (%d/%d)        -->    %s"%(number, self.start+number+1, self.to_be_exec,  interfaces.exploit.results[info.result])
			if self.logenable:
				filename = os.path.join(log_full,"%d.log"%number)
				info.write_to_file(filename)
				info.messages.clear()
			return True

		if self.exec_info:
			print self.color("==================================================", self.maincolor)
			print "%s %s"%(self.color("Exploit name:", self.maincolor),self.e.exploit.name)
			print "%s %s"%(self.color("Target address:", self.maincolor), self.e.getTargetHost()[0])
			print self.color("Exploit Parameters:", self.maincolor)
			for par in self.e.exploit.get_parameters_names():
				print"  %s = %s"%(par,self.e.exploit.get_parameter_value(par))
			print self.color("==================================================", self.maincolor)
			print "%s %s"%(self.color("Mutant Factory:",self.maincolor),self.e.factory.get_name())
			print "%s %d"%(self.color("Number of mutants:",self.maincolor),self.e.factory.count())
			print self.color("==================================================",self.maincolor)
			
			tot_number  = 1
			selected = self.e.opmanager.get_selected_operators()
			for y in selected:
				tot_number *= (1+y.params_combinations())
				
			print "%s"%self.color("Mutation space size: %d"%tot_number, self.maincolor)
			print "%s"%self.color("Operators:",self.maincolor)
			for op in self.e.opmanager.get_selected_operators():
				#print "%s:"%group
				#for op in oplist:
				print " [%s] - %s"%(op.group,op.name)
			print self.color("==================================================", self.maincolor)
					
		if self.exec_run:
			if self.callback == None:
				callback = local_callback
			else:
				callback = self.callback
			
			try:
				#sys.stdout.write("Mutant %d (%d/%d)        -->    "%(start,0,to_be_exec))
				sys.stdout.flush()
				self.e.execute(self.to_be_exec, self.start, self.sleep_time, callback)
			except Exception, msg:
				print msg
			#print "\r                                                       "
			for c in self.e.get_selected_collectors():
				ids = c.get_name()
				for m,a in c.get_alerts().items():
					if m == "uncorrelated":
						if len(a)>0:
							print "%d uncorrelated alerts"%len(a)
					elif len(a)==0:
						print self.color("Mutant %s evaded detection !!"%m,RED)
					else:
						filename = os.path.join(log_full,"%s.%s"%(m,ids))
						f = open(filename,"w")
						for l in a:
							f.write(l);
						f.close()
		self.e.clean_up()


if __name__ == '__main__':
	cl = CLInterface()
	if cl.parse_options()== False:
		sys.exit(1)
	cl.run()

