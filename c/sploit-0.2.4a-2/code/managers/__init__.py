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

# Author:       Davide Balzarotti
# File version: $Id: __init__.py 109 2006-02-27 20:17:42Z balzarot $

"""
	This package contains the Protocol Managers
	Each manager is in charge on managing a protocol or a piece of attack that
	needs to be automatically modified by sploit (e.g. the shellcode).
"""

__all__ = ["ip", "tcp", "eth", "ftp", "http", "imap", "egg"]
