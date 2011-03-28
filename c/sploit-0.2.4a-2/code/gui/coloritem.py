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
# $Id: coloritem.py 109 2006-02-27 20:17:42Z balzarot $

from qt import *
from qttable import *

class ColorItem(QTableItem):
	def __init__(self, table, edittype, text, color, alignment):
		QTableItem.__init__(self,table,edittype,text)
		self.color = color
		self.align = alignment

	def paint(self, painter, colorgroup, rect, selected):
		cg = QColorGroup(colorgroup)
		cg.setColor(QColorGroup.Base, self.color)
		QTableItem.paint(self,painter, cg, rect, selected)

	def alignment(self):
		return self.align 
