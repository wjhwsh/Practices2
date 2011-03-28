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
# $Id: ids_w.py 109 2006-02-27 20:17:42Z balzarot $

import sys,string
from qt import *
from qttable import *
from coloritem import ColorItem

import utils

class MyCheckItem(QCheckListItem):
	def __init__(self, parent, name, collector, engine):
		QCheckListItem.__init__(self, parent, name, QCheckListItem.CheckBox)
		self.collector = collector
		self.engine = engine
		
	def stateChange(self, val):
		if val == True:
			self.engine.add_collector(self.collector)
		else:
			self.engine.remove_collector(self.collector)
			
class IDSWidget(QVBox):
	
	def __init__( self, parent, engine):
		QWidget.__init__( self, parent, None )
		self.engine      = engine
		
		split = QSplitter(Qt.Vertical, self)
		self.list_view = QListView(split)
		self.list_view.setSortColumn(-1)

		self.list_view.setMinimumSize(500, 300)
		self.list_view.setTreeStepSize(15)
		#self.catalog_list.setSelectionMode(1)
		self.list_view.setAllColumnsShowFocus(True)
		self.list_view.setRootIsDecorated(1)
		self.list_view.addColumn("IDS Alerts Collector")
		self.list_view.setColumnWidth(0,300)

		for temp in utils.load_collectors_list("./collectors"):
			item = MyCheckItem(self.list_view, temp.get_name(), temp, self.engine)
		
		self.connect( self.list_view, SIGNAL( 'clicked( QListViewItem * )' ), self.properties )
		
		self.table = QTable(0, 3, split)
		self.table.setLeftMargin(0)

		header = self.table.horizontalHeader()
		header.setLabel(0, "Parameter", 140)
		header.setLabel(1, "Value", 200)
		header.setLabel(2, "Description", 350)
		header.setMovingEnabled(False)	
		
		self.connect( self.table, SIGNAL( 'valueChanged( int, int )' ), self.change_option )
		
		sizes = split.sizes()
		tot = sizes[0]+sizes[1]
		split.setSizes([tot*0.8,tot*0.2])

	def change_option(self, x,y):
		value = str(self.table.text(x,y))
		param = str(self.table.text(x,0))
		try:
			self.item.collector.set_parameter_value(param,eval(value))
		except Exception, msg:
			QMessageBox.warning(self, "Parameter Error",str(msg))
			self.properties(self.item)
			return
	
	def properties(self, item):
		self.table.setNumRows(0)
		if hasattr(item, 'collector') == False:
			return
		
		self.item = item		
		params = item.collector.get_parameters()
		self.table.setNumRows(len(params))
		row = 0
		for p in params:
			self.table.setRowHeight(row,30)
			colit = ColorItem(self.table, QTableItem.Never, p.name, QColor(170,220,170),0)
			self.table.setItem(row, 0, colit)
			value = p.value
			if type(value) is str:
				value = "%r"%value
			else:
				value = "%s"%value
			self.table.setText(row, 1, value)
			self.table.setItem(row, 2, QTableItem(self.table, QTableItem.Never, p.description))
			row += 1		
		
	def enter(self):
		pass
	
	def exit(self):
		return True
	
