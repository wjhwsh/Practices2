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
# $Id: execute_w.py 109 2006-02-27 20:17:42Z balzarot $

import sys, string, time, thread
from execinfo_dialog import ExecInfoDialog
from qt import *

import logger
import engine
import utils

class ExecuteWidget(QVBox):
	
	def __init__( self, parent, engine):
		QWidget.__init__( self, parent, None )
		self.engine   = engine
		self.running = False
		self.cont    = True
		
		self.fake_execution = False
		
		self.setMargin( 10 )
		self.setSpacing( 15 )
		
		oriz = QHBox( self )
		oriz.setSpacing( 15 )
		
		modebox  = QGroupBox(8, QGroupBox.Vertical,"Mutant Generation", oriz)
		
		QLabel('Number of possible Mutants', modebox)
		
		self.lcd = QLCDNumber( 8, modebox )
		self.lcd.display( self.engine.factory.count() )
		self.lcd.setSegmentStyle( QLCDNumber.Filled )
		self.lcd.setFixedHeight(50)
		#self.lcd.setMaximumWidth(250)
		
		QLabel('Mutant Factory:', modebox)
		self.factory_name = QLabel('None',modebox)
		self.factory_name.setText(self.engine.factory.get_name())
		self.openB  = QPushButton( "...", modebox )
		self.connect( self.openB,  SIGNAL("clicked()"), self.change_factory )
			
		numberbox  = QGroupBox(8, QGroupBox.Vertical, "Execution", oriz)

		temp = QHBox(numberbox)
		lab  = QLabel('Execute ',temp)
		self.numberLine = QSpinBox( 0, 1, 1, temp )
		self.numberLine.setSpecialValueText("ALL")
		self.numberLine.setMinimumWidth(100)
		lab2 = QLabel(' mutants', temp)
		
		temp = QHBox(numberbox)
		lab3 = QLabel('Starting from ',temp)
		self.firstLine = QSpinBox( 0, 0, 1, temp )
		self.firstLine.setMinimumWidth(100)
		end = QLabel("",temp)
		temp.setStretchFactor(end,50)
		
		temp = QHBox(numberbox)
		lab = QLabel('Sleep time between mutants (sec) ',temp)
		lab.setMinimumWidth(435)
		self.sleepLine = QSpinBox( 1, 100, 1, temp )
		self.sleepLine.setMinimumWidth(100)
		end = QLabel("",temp)
		temp.setStretchFactor(end,50)

		temp = QHBox(numberbox)
		lab = QLabel('Log level ',temp)
		lab.setMinimumWidth(278)
		self.ifcombo = QComboBox( False, temp, "" )
		self.ifcombo.insertItem( "DEBUG (very verbose)" )
		self.ifcombo.insertItem( "INFO" )
		self.ifcombo.insertItem( "WARNING" )
		self.ifcombo.insertItem( "ERROR" )
		self.ifcombo.setCurrentItem(3)
		self.connect( self.ifcombo, SIGNAL("activated(int)"), self.select_loglevel )
		end = QLabel("",temp)
		temp.setStretchFactor(end,50)
		
		o2 = QHBox( self )
		self.progress = QProgressBar(10,o2)
		self.startB = QPushButton('START',o2)
		
		self.connect( self.startB, SIGNAL("clicked()"), self.start )	
		
		self.results = QListView(self)
		self.results.setAllColumnsShowFocus(True)
		self.results.addColumn('Mutation',100)	
		self.results.addColumn('Result',150)
		self.connect( self.results, SIGNAL( 'doubleClicked( QListViewItem * )' ), self.properties )		
		self.results.setSortColumn(-1)
	
	def enter(self):
		self.engine.factory.reset()
		self.lcd.display (self.engine.factory.count())
		if self.engine.exploit == None:
			self.startB.setEnabled(False) 
		else:
			self.startB.setEnabled(True) 
		self.factory_name.setText(self.engine.factory.get_name())
		self.results.removeColumn(0)
		self.results.removeColumn(0)
		self.results.removeColumn(0)
		self.results.removeColumn(0)
		self.results.clear()
		self.results.setAllColumnsShowFocus(True)
		self.results.addColumn('Mutation',100)	
		self.results.addColumn('Result',150)
		for c in self.engine.get_selected_collectors():
			self.results.addColumn(c.get_name(),200)

	def refresh_list(self):
		i        = self.results.firstChild()
		ids_list = [] 
		for x in range(2,self.results.columns()):
			ids_list.append([x, str(self.results.columnText(x))])
			
		collectors = self.engine.get_selected_collectors()
		
		while i != None:
			i.execinfo.alerts = {}
			for ids in ids_list:
				collector = None
				for c in collectors:
					if c.get_name() == ids[1]:
						collector = c
						break
				if collector == None:
					return
				try:
					alerts = collector.get_alerts(i.execinfo.number)
					i.execinfo.alerts[ids[1]] = alerts
					n = len(alerts)
					if n > 0:
						i.setText(ids[0],str(n)+" alerts")
					else:
						i.setText(ids[0],"EVADED")
				except Exception, msg:
					if i.execinfo.result == 1:
						i.setText(ids[0],"EVADED")
					else:
						i.setText(ids[0],"Error")
					
				#print "%n %n"%(ids[0], len(alerts[ids[1]]))
			i = i.itemBelow()

	def exit(self):
		if self.running:
			return False
		return True
	
	def select_loglevel(self, n):
		logger.main.setLevel(n+1)
			
	def change_factory(self):
		filename = QFileDialog.getOpenFileName('factories','Factory (*.py)',self,'Open File','Load Mutant Factory')
		filename = str(filename)
		if len(filename) < 1:
			return
		temp = utils.load_factory(filename)
		self.engine.set_factory(temp)
		if self.engine.factory == None:
			self.lcd.display (1)
			self.firstLine.setMaxValue(0)
			self.numberLine.setMaxValue(1)
		else: 
			n = self.engine.factory.count()
			self.lcd.display (n) 
			self.firstLine.setMaxValue(n-1)
			self.numberLine.setMaxValue(n)
			self.factory_name.setText(self.engine.factory.get_name())

	
	def thread(self, num, first, sleep):
		try:
			if self.fake_execution:
				self.engine.fake_execute(num, first, sleep, self.callback)
			else:
				self.engine.execute(num, first, sleep, self.callback)
		except Exception, msg:
			print msg
		self.numberLine.setEnabled(True)
		self.firstLine.setEnabled(True)
		self.sleepLine.setEnabled(True)
		self.openB.setEnabled(True)
		self.refresh_list()
		self.running = False
		self.startB.setText('START')
		
	def start(self):
		if self.running == False:
			num   = str(self.numberLine.text())
			if num=="ALL":
				num = self.engine.factory.count()
			else:
				num = int(num)
			first = int(str(self.firstLine.text()))
			sleep = int(str(self.sleepLine.text()))
				
			self.results.clear()
			self.progress.setProgress(0,num)
			self.running = True
			self.cont    = True
			self.startB.setText('CANCEL')
			self.numberLine.setEnabled(False)
			self.firstLine.setEnabled(False)
			self.sleepLine.setEnabled(False)
			self.openB.setEnabled(False)
			
			thread.start_new_thread(self.thread, (num, first, sleep))
		else:
			self.cont = False
			
	def callback(self, number, info):
		self.progress.setProgress(self.progress.progress()+1)
		result = 'OK'
		if info.result == 2:
			result = 'ERROR'
		elif info.result == 3:
			result = 'FAIL'
		elif info.result == 4:
			result = '??'

		temp = ''
		#for o in info.operators:
		#	temp += o.name
		#	temp += '['
		#	for p in o.get_parameters():
		#		temp += "%s = %r"%(p.name,p.value)
		#	temp += ']  --  '
			
		newitem = QListViewItem(self.results, str(number), result)
		info.alerts = {}
		newitem.execinfo = info
		newitem.execnumber = number
		return self.cont

	def properties(self, item):
		p = ExecInfoDialog(self, item.execnumber, item.execinfo)
		p.setGeometry(200,200,700,700)
		p.show()





