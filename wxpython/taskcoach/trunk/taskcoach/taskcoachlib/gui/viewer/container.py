'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2011 Task Coach developers <developers@taskcoach.org>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import wx
from taskcoachlib import patterns
from taskcoachlib.gui import menu
import taskcoachlib.thirdparty.aui as aui


class ViewerContainer(object):
    ''' ViewerContainer is a container of viewers. It has a containerWidget
        that displays the viewers. The containerWidget is assumed to be 
        an AUI managed frame. The ViewerContainer knows which of its viewers
        is active and dispatches method calls to the active viewer or to the
        first viewer that can handle the method. This allows other GUI 
        components, e.g. menu's, to talk to the ViewerContainer as were
        it a regular viewer. '''
        
    def __init__(self, containerWidget, settings, *args, **kwargs):
        self.containerWidget = containerWidget
        self.registerEventHandlers()
        self._settings = settings
        self.viewers = []
        super(ViewerContainer, self).__init__(*args, **kwargs)
        
    def advanceSelection(self, forward):
        if len(self.viewers) <= 1:
            return # Not enough viewers to advance selection
        activeViewer = self.activeViewer()
        curSelection = self.viewers.index(activeViewer) if activeViewer else 0
        minSelection, maxSelection = 0, len(self.viewers) - 1
        if forward:
            newSelection = curSelection + 1 if minSelection <= curSelection < maxSelection else minSelection
        else:
            newSelection = curSelection - 1 if minSelection < curSelection <= maxSelection else maxSelection
        self.activateViewer(self.viewers[newSelection])
        
    def isViewerContainer(self):
        return True

    def registerEventHandlers(self):
        self.containerWidget.Bind(aui.EVT_AUI_PANE_CLOSE, self.onPageClosed)
        self.containerWidget.Bind(aui.EVT_AUI_PANE_ACTIVATED, self.onPageChanged)
        self.containerWidget.Bind(aui.EVT_AUI_PANE_FLOATED, self.onPageFloated)
    
    def __getitem__(self, index):
        return self.viewers[index]
    
    def __len__(self):
        return len(self.viewers)

    def addViewer(self, viewer):
        self.containerWidget.addPane(viewer, viewer.title())
        self.viewers.append(viewer)
        if len(self.viewers) == 1:
            self.activateViewer(viewer)
        patterns.Publisher().registerObserver(self.onSelect, 
            eventType=viewer.selectEventType(), eventSource=viewer)
        
    def closeViewer(self, viewer):
        if viewer == self.activeViewer():
            self.advanceSelection(False)
        pane = self.containerWidget.manager.GetPane(viewer)
        self.containerWidget.manager.ClosePane(pane)

    @classmethod
    def selectEventType(class_):
        ''' Events of this type are fired by the viewer container whenever the
            current selection of the active viewer changes. '''
        return '%s.select'%class_
    
    @classmethod
    def viewerChangeEventType(class_):
        ''' Events of this type are fired by the viewer container whenever the
            active viewer changes. '''
        return '%s.viewerChange'%class_
    
    def __getattr__(self, attribute):
        ''' Forward unknown attributes to the active viewer or the first
            viewer if there is no active viewer. '''
        return getattr(self.activeViewer() or self.viewers[0], attribute)

    def activeViewer(self):
        ''' Return the active viewer. '''
        allPanes = self.containerWidget.manager.GetAllPanes()
        for pane in allPanes:
            if pane.IsToolbar():
                continue
            if pane.HasFlag(pane.optionActive):
                if pane.IsNotebookControl():
                    notebook = aui.GetNotebookRoot(allPanes, pane.notebook_id)
                    return notebook.window.GetCurrentPage()
                else:
                    return pane.window
        return None
        
    def activateViewer(self, viewerToActivate):
        self.containerWidget.manager.ActivatePane(viewerToActivate)
        paneInfo = self.containerWidget.manager.GetPane(viewerToActivate)
        if paneInfo.IsNotebookPage():
            self.containerWidget.manager.ShowPane(viewerToActivate, True)

    def __del__(self):
        pass # Don't forward del to one of the viewers.
    
    def onSelect(self, event):
        patterns.Event(self.selectEventType(), self, *event.values()).send()

    def onPageChanged(self, event):
        patterns.Event(self.viewerChangeEventType(), self).send()
        self._ensureActiveViewerHasFocus()
        event.Skip()            
        
    def _ensureActiveViewerHasFocus(self):
        if not self.activeViewer():
            return
        window = wx.Window.FindFocus()
        while window:
            if window == self.activeViewer():
                break
            window = window.GetParent()
        else:
            wx.CallAfter(self.activeViewer().SetFocus)

    def onPageClosed(self, event):
        if event.GetPane().IsToolbar():
            return
        window = event.GetPane().window
        if hasattr(window, 'GetPage'):
            # Window is a notebook, close each of its pages
            for pageIndex in range(window.GetPageCount()):
                self._closeViewer(window.GetPage(pageIndex))
        else:
            # Window is a viewer, close it
            self._closeViewer(window)
        # Make sure we have an active viewer
        if not self.activeViewer():
            self.activateViewer(self.viewers[0])
        event.Skip()
        
    def _closeViewer(self, viewer):
        # When closing an AUI managed frame, we get two close events, 
        # be prepared:
        if viewer in self.viewers:
            self.viewers.remove(viewer)
            viewer.detach()
        
    def onPageFloated(self, event):
        ''' Give floating pane accelerator keys for activating next and previous
            viewer. '''
        viewer = event.GetPane().window
        table = wx.AcceleratorTable([(wx.ACCEL_CTRL, wx.WXK_PAGEDOWN, menu.activateNextViewerId),
                                     (wx.ACCEL_CTRL, wx.WXK_PAGEUP, menu.activatePreviousViewerId)])
        viewer.SetAcceleratorTable(table)
