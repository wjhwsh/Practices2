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
from taskcoachlib import patterns, command, meta, notify
from taskcoachlib.domain import date
from taskcoachlib.gui.dialog import reminder, editor
from taskcoachlib.i18n import _


class ReminderController(object):
    def __init__(self, mainWindow, taskList, effortList, settings):
        super(ReminderController, self).__init__()
        patterns.Publisher().registerObserver(self.onSetReminder,
            eventType='task.reminder')
        patterns.Publisher().registerObserver(self.onAddTask,
            eventType=taskList.addItemEventType(),
            eventSource=taskList)
        patterns.Publisher().registerObserver(self.onRemoveTask,
            eventType=taskList.removeItemEventType(),
            eventSource=taskList)
        patterns.Publisher().registerObserver(self.onWake, eventType='powermgt.on')
        self.__tasksWithReminders = {} # {task: reminderDateTime}
        self.__mainWindow = mainWindow
        self.__mainWindowWasHidden = False
        self.__registerRemindersForTasks(taskList)
        self.settings = settings
        self.taskList = taskList
        self.effortList = effortList

    def onAddTask(self, event):
        self.__registerRemindersForTasks(event.values())
                
    def onRemoveTask(self, event):
        self.__removeRemindersForTasks(event.values())
                
    def onSetReminder(self, event):
        tasks = event.sources()
        self.__removeRemindersForTasks(tasks)
        self.__registerRemindersForTasks(tasks)
        
    def onWake(self, event):
        self.showReminderMessages(date.DateTime.now())
        
    def onReminder(self, event):
        self.showReminderMessages(event.value())
        
    def showReminderMessages(self, now):
        now += date.TimeDelta(seconds=5) # Be sure not to miss reminders 
        requestUserAttention = False
        for task, reminderDateTime in self.__tasksWithReminders.items():
            if reminderDateTime <= now:
                requestUserAttention = True
                self.showReminderMessage(task)
        if requestUserAttention:
            self.requestUserAttention()        
        
    def showReminderMessage(self, task, ReminderDialog=reminder.ReminderDialog):
        notifier = self.settings.get('feature', 'notifier')
        if notifier != 'Task Coach' and notify.AbstractNotifier.get(notifier) is not None:
            notify.AbstractNotifier.get(notifier).notify(_('%s Reminder') % meta.name, task.subject(),
                                                         wx.ArtProvider.GetBitmap('taskcoach', size=wx.Size(32, 32)),
                                                         windowId=self.__mainWindow.GetHandle())
            self.__removeReminder(task)
            task.setReminder(None)
        else:
            reminderDialog = ReminderDialog(task, self.taskList, self.effortList, self.settings, self.__mainWindow)
            reminderDialog.Bind(wx.EVT_CLOSE, self.onCloseReminderDialog)        
            reminderDialog.Show()
            self.__removeReminder(task)    
        
    def onCloseReminderDialog(self, event, show=True):
        event.Skip()
        dialog = event.EventObject
        task = dialog.task
        if not dialog.ignoreSnoozeOption:
            snoozeOptions = dialog.snoozeOptions
            snoozeTimeDelta = snoozeOptions.GetClientData(snoozeOptions.Selection)
            if snoozeTimeDelta:
                newReminder = date.DateTime.now() + snoozeTimeDelta
            else:
                newReminder = None
            task.setReminder(newReminder) # Note that this is not undoable
            # Undoing the snoozing makes little sense, because it would set the 
            # reminder back to its original date-time, which is now in the past.
        if dialog.openTaskAfterClose:
            editTask = editor.TaskEditor(self.__mainWindow, [task], 
                self.settings, self.taskList, self.__mainWindow.taskFile, 
                bitmap='edit')
            editTask.Show(show)
        else:
            editTask = None
        dialog.Destroy()
        if self.__mainWindowWasHidden:
            self.__mainWindow.Hide()
        return editTask # For unit testing purposes

    def requestUserAttention(self):
        notifier = self.settings.get('feature', 'notifier')
        if notifier != 'Native' and notify.AbstractNotifier.get(notifier) is not None:
            # When using Growl/Snarl, this is not necessary. Even when not using Growl, it's
            # annoying as hell. Anyway.
            return
        self.__mainWindowWasHidden = not self.__mainWindow.IsShown()
        if self.__mainWindowWasHidden:
            self.__mainWindow.Show()
        if not self.__mainWindow.IsActive():
            self.__mainWindow.RequestUserAttention()
            
    def __registerRemindersForTasks(self, tasks):
        for task in tasks:
            if task.reminder():
                self.__registerReminder(task)

    def __removeRemindersForTasks(self, tasks):
        for task in tasks:
            if task in self.__tasksWithReminders:
                self.__removeReminder(task)

    def __registerReminder(self, task):
        reminderDateTime = task.reminder()
        if reminderDateTime < date.DateTime.now():
            reminderDateTime = date.DateTime.now() + date.TimeDelta(seconds=2)
        if reminderDateTime not in self.__tasksWithReminders.values():
            self.__changeDateTimeObservation(reminderDateTime, 
                                             'registerObserver')
        self.__tasksWithReminders[task] = reminderDateTime
            
    def __removeReminder(self, task):
        oldReminderDateTime = self.__tasksWithReminders[task]
        del self.__tasksWithReminders[task]
        if oldReminderDateTime not in self.__tasksWithReminders.values():
            self.__changeDateTimeObservation(oldReminderDateTime, 
                                             'removeObserver')
    
    def __changeDateTimeObservation(self, reminderDateTime, registrationMethod):
        eventType = date.Clock().eventType(reminderDateTime)
        getattr(patterns.Publisher(), registrationMethod)(self.onReminder, 
            eventType=eventType)

