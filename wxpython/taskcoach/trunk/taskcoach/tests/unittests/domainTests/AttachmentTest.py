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

import os
import test
from taskcoachlib import patterns
from taskcoachlib.domain import attachment


class GetRelativePathTest(test.TestCase):
    def testBaseAndPathEqual(self):
        self.assertEqual('', attachment.getRelativePath('/test', '/test'))
        
    def testPathIsSubDirOfBase(self):
        self.assertEqual('subdir', attachment.getRelativePath('/test/subdir', '/test'))

    def testBaseIsSubDirOfPath(self):
        self.assertEqual('..', attachment.getRelativePath('/test', '/test/subdir'))
        
    def testBaseAndPathAreDifferent(self):
        self.assertEqual(os.path.join('..', 'bar'),
                         attachment.getRelativePath('/bar', '/foo'))
        
        
class FileAttachmentTest(test.TestCase):
    def setUp(self):
        self.filename = ''
        self.attachment = attachment.FileAttachment('filename')
        self.events = []
        
    def onEvent(self, event):
        self.events.append(event)
        
    def openAttachment(self, filename):
        self.filename = filename
        
    def testCreateFileAttachment(self):
        self.assertEqual('filename', self.attachment.location())
        
    def testOpenFileAttachmentWithRelativeFilename(self):
        self.attachment.open(openAttachment=self.openAttachment)
        self.assertEqual('filename', self.filename)
        
    def testOpenFileAttachmentWithRelativeFilenameAndWorkingDir(self):
        self.attachment.open('/home', openAttachment=self.openAttachment)
        self.assertEqual(os.path.normpath(os.path.join('/home', 'filename')), 
                         self.filename)
        
    def testOpenFileAttachmentWithAbsoluteFilenameAndWorkingDir(self):
        att = attachment.FileAttachment('/home/frank/attachment.txt')
        att.open('/home/jerome', openAttachment=self.openAttachment)
        self.assertEqual(os.path.normpath(os.path.join('/home/frank/attachment.txt')), 
                         self.filename)
                                
    def testCopy(self):
        copy = self.attachment.copy()
        # pylint: disable-msg=E1101
        self.assertEqual(copy.location(), self.attachment.location())
        self.attachment.setDescription('new')
        self.assertEqual(copy.location(), self.attachment.location())

    def testLocationNotification(self):
        eventType = self.attachment.locationChangedEventType()
        patterns.Publisher().registerObserver(self.onEvent, eventType)
        self.attachment.setLocation('new location')
        self.assertEqual([patterns.Event(eventType, self.attachment, 
                                         'new location')], 
                         self.events)

    def testModificationEventTypes(self):
        Attachment = attachment.Attachment
        # pylint: disable-msg=E1101
        self.assertEqual([Attachment.notesChangedEventType(),
                          Attachment.subjectChangedEventType(),
                          Attachment.descriptionChangedEventType(),
                          Attachment.foregroundColorChangedEventType(),
                          Attachment.backgroundColorChangedEventType(),
                          Attachment.fontChangedEventType(),
                          Attachment.iconChangedEventType(),
                          Attachment.selectedIconChangedEventType(),
                          Attachment.locationChangedEventType()], 
                         Attachment.modificationEventTypes())
