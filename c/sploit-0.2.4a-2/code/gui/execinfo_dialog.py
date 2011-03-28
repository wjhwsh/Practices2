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
# $Id: execinfo_dialog.py 109 2006-02-27 20:17:42Z balzarot $

from qt import *
from qttable import *

output = """
	<br>
	<font size=+2><center><b>MUTANT # %d</b></center></font>
	<br>
	<table width = "100%%">
		<tr bgcolor = "#d0d0d0">
		<td>
			<b>Result:</b> %s
		</td>
		</tr>
		<tr>
		<tr>
		<td>
			<b>Date:</b> %s
		</td>
		</tr>
		<tr bgcolor = "#d0d0d0">
		<td>
			<b>Execution time:</b> %.2f sec
		</td>
		</tr>
		<tr>
		<tr>		
		<td>
			<b>Mutant Operators:</b><br>
			%s
		</td>
		</tr>
		<tr bgcolor = "#d0d0d0">
		<td>
			<b>TCP ports: </b> %s
		</td>
		</tr>
		<tr>
		<td>
			<b>UDP ports: </b> %s
		</td>
		</tr>		
		<tr bgcolor = "#d0d0d0">
		<td>
			<b>Alerts:</b><br>
			%s
		</td>
		</tr>
		<tr>
		<td>
			<b>Debug Messages:</b><br>
			%s
		</td>
		</tr>
	</table>
	"""

class ExecInfoDialog(QDialog):
	def __init__(self, parent, number, info):
		QDialog.__init__( self, parent, None )
		self.layout = QHBoxLayout(self)
		self.result = QTextBrowser(self)
		#self.result.setFixedHeight(600)
		#self.result.setFixedWidth(800)
		#self.result.mimeSourceFactory().setFilePath(QStringList(("./pictures")))
		temp = "<ul>"
		for o in info.operators:
			temp += "<li>"+o.name+" "
			if len(o.get_parameters()) == 0:
				continue
			temp += '['
			for p in o.get_parameters():
				temp += "%s = %r "%(p.name,p.value)
			temp += ']'
		temp += "</ul>"
		
		msg = info.messages.getText()
		msg = msg.replace("\n","<br>")

		tcp_ports = ""		
		if info.tcp_ports[0] == 0:
			tcp_ports = "None"
		else:
			if info.tcp_ports[0] == info.tcp_ports[1]:
				tcp_ports = "%d"%info.tcp_ports[0]
			else:
				tcp_ports = "%d - %d"%(info.tcp_ports[0], info.tcp_ports[1])

		udp_ports = ""		
		if info.udp_ports[0] == 0:
			udp_ports = "None"
		else:
			if info.udp_ports[0] == info.udp_ports[1]:
				udp_ports = "%d"%info.udp_ports[0]
			else:
				udp_ports = "%d - %d"%(info.udp_ports[0], info.udp_ports[1])
		
		alerts_msg = ""
		for a in info.alerts.items():
			alerts_msg += "<b>%s</b> (%d alerts)<br>"%(a[0], len(a[1]))
			if len(a[1]) > 0:
				alerts_msg += "<ul>"
				for x in a[1]:
					alerts_msg += "<li> %s"%x.replace("\n","<br>")
				alerts_msg += "</ul>"
		
		result = 'OK'
		if info.result == 2:
			result = 'ERROR'
		elif info.result == 3:
			result = 'FAIL'
		elif info.result == 4:
			result = 'Unable to get the result'
			
		self.result.setText(output%(number, result, info.date, info.exectime, temp, tcp_ports, udp_ports, alerts_msg, msg))
		self.layout.addWidget(self.result)
