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
# $Id: mutation_w.py 109 2006-02-27 20:17:42Z balzarot $

import sys,string
from qt import *
from qttable import *
from coloritem import ColorItem


class MyCheckItem(QCheckListItem):
	def __init__(self, parent, name, operator, engine):
		QCheckListItem.__init__(self, parent, name, QCheckListItem.CheckBox)
		self.mutant_operator = operator
		self.engine = engine
		
	def stateChange(self, val):
		if val == True:
			self.engine.opmanager.select_operator(self.mutant_operator)
		else:
			self.engine.opmanager.unselect_operator(self.mutant_operator)


class MutationWidget(QVBox):
	
	def __init__( self, parent, engine):
		QWidget.__init__( self, parent, None )
		self.engine      = engine
		
		split = QSplitter(Qt.Vertical,self)
		temph = QHBox(split)
		self.list_view = QListView(temph)
		self.list_view.setSortColumn(-1)
		self.list_view.setMinimumSize(500, 300)
		self.list_view.setTreeStepSize(15)
		self.list_view.setAllColumnsShowFocus(True)
		self.list_view.setRootIsDecorated(1)
		self.list_view.addColumn("Mutant Operator")
		self.list_view.setColumnWidth(0,300)
		self.list_view.addColumn("Combinations of Parameters")

		tempv = QVBox(temph)
		self.upbutton = QPushButton( "Move &Up", tempv )
		self.connect( self.upbutton,  SIGNAL("clicked()"), self.moveup )
		self.downbutton = QPushButton( "Move &Down", tempv )
		self.connect( self.downbutton,  SIGNAL("clicked()"), self.movedown )
		
		opnumber = self.update_list()
		
		self.parentWidget().parentWidget().statusBar().message("%d mutant operators loaded"%opnumber, 5000 )
				
		self.connect( self.list_view, SIGNAL( 'clicked( QListViewItem * )' ), self.properties )
		
		self.table = QTable(0, 4, split)
		self.table.setLeftMargin(0)

		header = self.table.horizontalHeader()
		header.setLabel(0, "Parameter", 140)
		header.setLabel(1, "Value", 150)
		header.setLabel(2, "Multiple Values",300)
		header.setLabel(3, "Description",300)
		header.setMovingEnabled(False)	
		
		self.connect( self.table, SIGNAL( 'valueChanged( int, int )' ), self.change_option )
		
		sizes = split.sizes()
		tot = sizes[0]+sizes[1]
		split.setSizes([tot*0.8,tot*0.2])

	def update_list(self):
		self.list_view.clear()
		opnumber = 0
		for group, ops in self.engine.opmanager.get_operators().iteritems():
			parent = QListViewItem(self.list_view, group)
			for op, sel in ops[::-1]:
				opnumber +=1
				item = MyCheckItem(parent,op.name,op,self.engine)
				item.setText(1,str(op.params_combinations()))
				if sel:
					item.setState(QCheckListItem.On)
		return opnumber

	def change_option(self, x,y):
		value = str(self.table.text(x,y))
		param = str(self.table.text(x,0))
		if y == 1:  # value
			try:
				self.item.mutant_operator.set_parameter_value(param,eval(value))
			except Exception, msg:
				QMessageBox.warning(self, "Parameter Error",str(msg))
				self.properties(self.item)
				return
		else:   	# multivalue
			#values = value.split(';')
			#res = []
			#for  v in values:
			#	v = v.strip()
			#	if v[0]=="'" and v[-1]=="'":
			#		v = v[1:-1]
			#	res.append(v)
			try:
				#self.item.mutant_operator.set_multiple_values(param,res)
				self.item.mutant_operator.set_multiple_values(param, eval(value))
			except Exception, msg:
				QMessageBox.warning(self, "Parameter Error",str(msg))
				self.properties(self.item)
				return
		
		self.item.setText(1,str(self.item.mutant_operator.params_combinations()))	
			
		
	def properties(self, item):
		self.table.setNumRows(0)
		if hasattr(item, 'mutant_operator') == False:
			return
		
		self.parentWidget().parentWidget().statusBar().message( item.mutant_operator.description, 4000 )
		self.item = item		
		params = item.mutant_operator.get_parameters()
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
			if p.is_multi_values():
				#multi = ''
				m = p.get_multiple_values()
				#for v in m:
				#	multi += '%r ; '%v
				#if multi[-3:] == " ; ":
				#	multi = multi[:-3]
				self.table.setText(row, 2, "%s"%m)
			else:
				self.table.setItem(row, 2, ColorItem(self.table, QTableItem.Never, "---",QColor(230,230,230),4))
			self.table.setItem(row, 3, QTableItem(self.table, QTableItem.Never, p.description))
			row += 1		
		
	def moveup(self):
		item = self.list_view.selectedItem()
		if (item == None) or (item.__class__ is QListViewItem):
			return
		prec = item.itemAbove()
		if (prec == item.parent()) or (prec.__class__ is MyCheckItem == False):
			return
		prec.moveItem(item)
		self.engine.opmanager.move_up(item.mutant_operator)

	def movedown(self):
		item = self.list_view.selectedItem()
		if (item == None) or (item.__class__ is QListViewItem):
			return
		next = item.nextSibling()
		if (next == None) or (next.__class__ is MyCheckItem == False):
			return
		item.moveItem(next)
		self.engine.move_operator_down(item.mutant_operator)
		
	def enter(self):
		self.list_view.clear()
		self.update_list()
		pass
#		self.list_view.clear()
#		for temp in self.engine.oplist.iteritems():
#			parent = QListViewItem(self.list_view, temp[0])
#			for op in temp[1]:
#				item = QCheckListItem(parent,op.name,1)
#				item.setText(1,'1')
#				item.mutant_operator = op
	
	def exit(self):
		return True
	
	def all(self):
		for i in self.operators:
			print i.text()
		
	def clear(self):
		for i in self.operators:
			i.setOn(False)
		
		
