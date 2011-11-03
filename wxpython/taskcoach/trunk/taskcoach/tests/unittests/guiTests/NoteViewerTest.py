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

import test
from taskcoachlib import gui, config, persistence
from taskcoachlib.domain import note, attachment, category


class NoteViewerTest(test.wxTestCase):
    def setUp(self):
        super(NoteViewerTest, self).setUp()
        self.settings = config.Settings(load=False)
        self.taskFile = persistence.TaskFile()
        self.note = note.Note()
        self.taskFile.notes().append(self.note)
        self.viewer = gui.viewer.NoteViewer(self.frame, self.taskFile, 
                                            self.settings, 
                                            notesToShow=self.taskFile.notes())

    def firstItem(self):
        widget = self.viewer.widget
        return widget.GetFirstChild(widget.GetRootItem())[0]

    def firstItemText(self, column=0):
        return self.viewer.widget.GetItemText(self.firstItem(), column)

    def firstItemIcon(self, column=0):    
        return self.viewer.widget.GetItemImage(self.firstItem(), column=column)

    def testLocalNoteViewerForItemWithoutNotes(self):
        localViewer = gui.viewer.NoteViewer(self.frame, self.taskFile, 
                                            self.settings, 
                                            notesToShow=note.NoteContainer())
        self.failIf(localViewer.presentation())
        
    def testShowDescriptionColumn(self):
        self.note.setDescription('Description')
        self.viewer.showColumnByName('description')
        self.assertEqual('Description', self.firstItemText(column=1))

    def testShowCategoriesColumn(self):
        newCategory = category.Category('Category')
        self.taskFile.categories().append(newCategory)
        self.note.addCategory(newCategory)
        newCategory.addCategorizable(self.note)
        self.viewer.showColumnByName('categories')
        self.assertEqual('Category', self.firstItemText(column=1))
        
    def testShowAttachmentColumn(self):
        self.viewer.showColumnByName('attachments')
        self.note.addAttachments(attachment.FileAttachment('whatever'))
        self.assertEqual(self.viewer.imageIndex['paperclip_icon'], 
                         self.firstItemIcon(column=1))

