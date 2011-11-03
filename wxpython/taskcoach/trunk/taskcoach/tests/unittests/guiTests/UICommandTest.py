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
import test
from unittests import dummy
from taskcoachlib import gui, config, persistence
from taskcoachlib.domain import task, category, date, attachment, effort
from taskcoachlib.thirdparty import desktop


if desktop.get_desktop() in ('KDE', 'GNOME'): # pragma: no cover
    # On a KDE desktop, kfmclient insists on showing an error message for 
    # non-existing files, even when passing --noninteractive, so we make sure 
    # kfmclient is not invoked at all. 
    # On a GNOME desktop, this launch replacement prevents an error message
    # to stderr when the file doesn't exist.
    import os
    os.environ['DESKTOP_LAUNCH'] = 'python -c "import sys, os; sys.exit(0 if os.path.exists(sys.argv[1]) else 1)"'


class UICommandTest(test.wxTestCase):
    def setUp(self):
        super(UICommandTest, self).setUp()
        self.uicommand = dummy.DummyUICommand(menuText='undo', bitmap='undo')
        self.menu = wx.Menu()
        self.frame = wx.Frame(None)
        self.frame.Show(False)
        self.frame.SetMenuBar(wx.MenuBar())
        self.frame.CreateToolBar()

    def activate(self, window, windowId):
        window.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, 
                                            windowId))

    def testAppendToMenu(self):
        menuId = self.uicommand.addToMenu(self.menu, self.frame)
        self.assertEqual(menuId, self.menu.FindItem(self.uicommand.menuText))

    def testAppendToToolBar(self):
        toolId = self.uicommand.appendToToolBar(self.frame.GetToolBar())
        self.assertEqual(0, self.frame.GetToolBar().GetToolPos(toolId))

    def testActivationFromMenu(self):
        menuId = self.uicommand.addToMenu(self.menu, self.frame)
        self.activate(self.frame, menuId)
        self.failUnless(self.uicommand.activated)

    def testActivationFromToolBar(self):
        menuId = self.uicommand.appendToToolBar(self.frame.GetToolBar())
        self.activate(self.frame.GetToolBar(), menuId)
        self.failUnless(self.uicommand.activated)


class wxTestCaseWithFrameAsTopLevelWindow(test.wxTestCase):
    def setUp(self):
        task.Task.settings = self.settings = config.Settings(load=False)
        wx.GetApp().SetTopWindow(self.frame)
        self.taskFile = self.frame.taskFile = persistence.TaskFile()


class NewTaskWithSelectedCategoryTest(wxTestCaseWithFrameAsTopLevelWindow):
    def setUp(self):
        super(NewTaskWithSelectedCategoryTest, self).setUp()
        self.categories = self.taskFile.categories()
        self.categories.append(category.Category('cat'))
        self.viewer = gui.viewer.CategoryViewer(self.frame, self.taskFile, 
                                                self.settings)
       
    def createNewTask(self):
        taskNew = gui.uicommand.NewTaskWithSelectedCategories( \
            taskList=self.taskFile.tasks(), viewer=self.viewer, 
            categories=self.categories, settings=self.settings)
        dialog = taskNew.doCommand(None, show=False)
        tree = dialog._interior[4].viewer.widget
        return tree.GetFirstChild(tree.GetRootItem())[0]

    def selectFirstCategory(self):
        self.viewer.select([list(self.categories)[0]])

    def testNewTaskWithSelectedCategory(self):
        self.selectFirstCategory()
        firstCategoryInTaskDialog = self.createNewTask()
        self.failUnless(firstCategoryInTaskDialog.IsChecked())
        
    def testNewTaskWithoutSelectedCategory(self):
        firstCategoryInTaskDialog = self.createNewTask()
        self.failIf(firstCategoryInTaskDialog.IsChecked())


class DummyTask(object):
    def subject(self, *args, **kwargs): # pylint: disable-msg=W0613
        return 'subject'
    
    def description(self):
        return 'description'


class DummyViewer(object):
    def __init__(self, selection=None, showingEffort=False, 
                 domainObjectsToView=None):
        self.selection = selection or []
        self.showingEffort = showingEffort
        self.domainObjects = domainObjectsToView
        
    def curselection(self):
        return self.selection

    def curselectionIsInstanceOf(self, class_):
        return self.selection and isinstance(self.selection[0], class_)
        
    def isShowingCategories(self):
        return self.selection and isinstance(self.selection[0], category.Category)

    def isShowingTasks(self):
        return False

    def isShowingEffort(self):
        return self.showingEffort
    
    def domainObjectsToView(self):
        return self.domainObjects


class MailTaskTest(test.TestCase):
    def testException(self):
        def mail(*args): # pylint: disable-msg=W0613
            raise RuntimeError, 'message'
        
        def showerror(*args, **kwargs): # pylint: disable-msg=W0613
            self.showerror = args # pylint: disable-msg=W0201
            
        mailTask = gui.uicommand.Mail(viewer=DummyViewer([DummyTask()]))
        mailTask.doCommand(None, mail=mail, showerror=showerror)
        self.assertEqual('Cannot send email:\nmessage', self.showerror[0])

    
class MarkCompletedTest(test.TestCase):
    def assertMarkCompletedIsEnabled(self, selection, shouldBeEnabled=True):
        viewer = DummyViewer(selection)
        markCompleted = gui.uicommand.TaskToggleCompletion(viewer=viewer)
        isEnabled = markCompleted.enabled(None)
        if shouldBeEnabled:
            self.failUnless(isEnabled)
        else:
            self.failIf(isEnabled)
            
    def testNotEnabledWhenSelectionIsEmpty(self):
        self.assertMarkCompletedIsEnabled(selection=[], shouldBeEnabled=False)
        
    def testEnabledWhenSelectedTaskIsNotCompleted(self):
        self.assertMarkCompletedIsEnabled(selection=[task.Task()])
        
    def testEnabledWhenSelectedTaskIsCompleted(self):
        self.assertMarkCompletedIsEnabled(
            selection=[task.Task(completionDateTime=date.Now())])
        
    def testEnabledWhenSelectedTasksAreBothCompletedAndUncompleted(self):
        self.assertMarkCompletedIsEnabled(
            selection=[task.Task(completionDateTime=date.Now()), task.Task()])


class TaskNewTest(wxTestCaseWithFrameAsTopLevelWindow):
    def testNewTaskWithCategories(self):
        cat = category.Category('cat', filtered=True)
        self.taskFile.categories().append(cat)
        taskNew = gui.uicommand.TaskNew(taskList=self.taskFile.tasks(), 
                                        settings=self.settings)
        dialog = taskNew.doCommand(None, show=False)
        tree = dialog._interior[4].viewer.widget
        firstChild = tree.GetFirstChild(tree.GetRootItem())[0]
        self.failUnless(firstChild.IsChecked())


class NoteNewTest(wxTestCaseWithFrameAsTopLevelWindow):
    def testNewNoteWithCategories(self):        
        cat = category.Category('cat', filtered=True)
        self.taskFile.categories().append(cat)
        noteNew = gui.uicommand.NoteNew(notes=self.taskFile.notes(), 
                                        settings=self.settings)
        dialog = noteNew.doCommand(None, show=False)
        tree = dialog._interior[1].viewer.widget
        firstChild = tree.GetFirstChild(tree.GetRootItem())[0]
        self.failUnless(firstChild.IsChecked())


class EffortNewTest(wxTestCaseWithFrameAsTopLevelWindow):
    def testNewEffortUsesTaskOfSelectedEffort(self):
        task1 = task.Task('task 1')
        task2 = task.Task('task 2')
        effort_task2 = effort.Effort(task2)
        task2.addEffort(effort_task2)
        self.taskFile.tasks().extend([task1, task2])
        viewer = DummyViewer(task2.efforts(), showingEffort=True, 
                             domainObjectsToView=self.taskFile.tasks())
        effortNew = gui.uicommand.EffortNew(effortList=self.taskFile.efforts(),
                                            taskList=self.taskFile.tasks(),
                                            viewer=viewer, 
                                            settings=self.settings)
        dialog = effortNew.doCommand(None, show=False)
        for eachEffort in dialog._items:
            self.assertEqual(task2, eachEffort.task())
        

class EditPreferencesTest(test.TestCase):
    def testEditPreferences(self):
        settings = config.Settings(load=False)
        editPreferences = gui.uicommand.EditPreferences(settings=settings)
        editPreferences.doCommand(None, show=False)
        # No assert, just checking whether it works without exceptions
        
        
class EffortViewerAggregationChoiceTest(test.TestCase):
    def setUp(self):
        self.selectedAggregation = 'details'
        self.showAggregationCalled = False
        self.choice = gui.uicommand.EffortViewerAggregationChoice(viewer=self)
        self.choice.currentChoice = 0
        class DummyEvent(object):
            def __init__(self, selection):
                self.selection = selection
            def GetInt(self):
                return self.selection
        self.DummyEvent = DummyEvent
        
    def showEffortAggregation(self, aggregation):
        self.selectedAggregation = aggregation
        self.showAggregationCalled = True
    
    def testUserPicksCurrentChoice(self):
        self.choice.onChoice(self.DummyEvent(0))
        self.failIf(self.showAggregationCalled)

    def testUserPicksSameChoiceTwice(self):
        self.choice.onChoice(self.DummyEvent(1))
        self.showAggregationCalled = False
        self.choice.onChoice(self.DummyEvent(1))
        self.failIf(self.showAggregationCalled)
    
    def testUserPicksEffortPerDay(self):
        self.choice.onChoice(self.DummyEvent(1))
        self.assertEqual('day', self.selectedAggregation)

    def testUserPicksEffortPerWeek(self):
        self.choice.onChoice(self.DummyEvent(2))
        self.assertEqual('week', self.selectedAggregation)

    def testUserPicksEffortPerMonth(self):
        self.choice.onChoice(self.DummyEvent(3))
        self.assertEqual('month', self.selectedAggregation)

    def testSetChoice(self):
        class DummyToolBar(wx.Frame):
            def AddControl(self, *args, **kwargs):
                pass
        self.choice.appendToToolBar(DummyToolBar(None))
        self.choice.setChoice('week')
        self.assertEqual('Effort per week',
                         self.choice.choiceCtrl.GetStringSelection())
        self.assertEqual(2, self.choice.currentChoice)


class OpenAllAttachmentsTest(test.TestCase):
    def setUp(self):
        settings = config.Settings(load=False)
        self.viewer = DummyViewer([task.Task('Task')])
        self.openAll = gui.uicommand.OpenAllAttachments(settings=settings, 
                                                        viewer=self.viewer)
        self.errorArgs = self.errorKwargs = None

    def showerror(self, *args, **kwargs): # pragma: no cover
        self.errorArgs = args
        self.errorKwargs = kwargs
        
    def testNoAttachments(self):
        self.openAll.doCommand(None)
        
    @test.skipOnPlatform('__WXMAC__')
    def testNonexistingAttachment(self): # pragma: no cover
        self.viewer.selection[0].addAttachment(attachment.FileAttachment('Attachment'))
        result = self.openAll.doCommand(None, showerror=self.showerror)
        # Don't test the error message itself, it differs per platform
        if self.errorKwargs:
            self.assertEqual(dict(caption='Error opening attachment',
                                  style=wx.ICON_ERROR), self.errorKwargs)
        else:
            self.assertNotEqual(0, result)
            
    def testMultipleAttachments(self):
        class DummyAttachment(object):
            def __init__(self):
                self.openCalled = False
            def open(self, attachmentBase): # pylint: disable-msg=W0613
                self.openCalled = True
            def isDeleted(self):
                return False
            
        dummyAttachment1 = DummyAttachment()
        dummyAttachment2 = DummyAttachment()
        self.viewer.selection[0].addAttachment(dummyAttachment1)
        self.viewer.selection[0].addAttachment(dummyAttachment2)
        self.openAll.doCommand(None)
        self.failUnless(dummyAttachment1.openCalled and dummyAttachment2.openCalled)


class ToggleCategoryTest(test.TestCase):
    def setUp(self):
        self.category = category.Category('Category')
        
    def testEnableWhenViewerIsShowingCategorizables(self):
        viewer = DummyViewer(selection=[task.Task('Task')])
        uiCommand = gui.uicommand.ToggleCategory(viewer=viewer,
                                                 category=self.category)
        self.failUnless(uiCommand.enabled(None))
        
    def testDisableWhenViewerIsShowingCategories(self):
        viewer = DummyViewer(selection=[self.category])
        uiCommand = gui.uicommand.ToggleCategory(viewer=viewer,
                                                 category=self.category)
        self.failIf(uiCommand.enabled(None))


class EffortStopTest(test.TestCase):
    def setUp(self):
        super(EffortStopTest, self).setUp()
        task.Task.settings = config.Settings(load=False)
        self.taskList = task.TaskList()
        self.task = task.Task('Task')
        self.task2 = task.Task('Task 2')
        self.effort1 = effort.Effort(self.task)
        self.effort2 = effort.Effort(self.task)
        self.taskList.append(self.task)
        self.effortStop = gui.uicommand.EffortStop(effortList=effort.EffortList(self.taskList),
                                                   taskList=self.taskList)
    
    # Tests of EffortStop.enabled()
        
    def testStopIsNotEnabledByDefault(self):
        self.failIf(self.effortStop.enabled())
        
    def testStopIsEnabledWhenEffortIsTracked(self):
        self.task.addEffort(self.effort1)
        self.failUnless(self.effortStop.enabled())

    def testStopResumeIsEnabledWhenEffortIsTracked(self):
        self.task.addEffort(self.effort1)
        self.effort1.setStop(date.Now())
        self.failUnless(self.effortStop.enabled())

    def testStopIsDisabledWhenEffortsIsDeleted(self):
        self.task.addEffort(self.effort1)
        self.task.removeEffort(self.effort1)
        self.failIf(self.effortStop.enabled())
        
    def testStopIsEnabledWhenTwoEffortsAreTracked(self):
        self.task.addEffort(self.effort1)
        self.task.addEffort(self.effort2)
        self.failUnless(self.effortStop.enabled())
        
    def testStopIsEnabledWhenOneOfTwoEffortsIsStopped(self):
        self.task.addEffort(self.effort1)
        self.task.addEffort(self.effort2)
        self.effort1.setStop(date.Now())
        self.failUnless(self.effortStop.enabled())

    def testStopIsEnabledWhenOneOfTwoEffortsIsDeleted(self):
        self.task.addEffort(self.effort1)
        self.task.addEffort(self.effort2)
        self.task.removeEffort(self.effort1)
        self.failUnless(self.effortStop.enabled())
        
    def testPauseIsEnabledWhenBothEffortsAreStopped(self):
        self.task.addEffort(self.effort1)
        self.task.addEffort(self.effort2)
        self.effort1.setStop(date.Now())
        self.effort2.setStop(date.Now())
        self.failUnless(self.effortStop.enabled())

    def testStopIsDisabledWhenBothEffortsAreDeleted(self):
        self.task.addEffort(self.effort1)
        self.task.addEffort(self.effort2)
        self.task.removeEffort(self.effort1)
        self.task.removeEffort(self.effort2)
        self.failIf(self.effortStop.enabled())
        
    def testStopIsDisabledWhenTaskIsDeleted(self):
        self.task.addEffort(self.effort1)
        self.taskList.remove(self.task)
        self.failIf(self.effortStop.enabled())

    def testStopIsEnabledWhenOneOfTwoTasksWithTrackedEffortIsDeleted(self):
        self.task.addEffort(self.effort1)
        self.task2.addEffort(effort.Effort(self.task2))
        self.taskList.append(self.task2)
        self.taskList.remove(self.task)
        self.failUnless(self.effortStop.enabled())
        
    def testStopIsEnabledWhenATaskWithTrackedEffortIsAdded(self):
        self.task2.addEffort(effort.Effort(self.task2))
        self.taskList.append(self.task2)
        self.failUnless(self.effortStop.enabled())
        
    def testStopIsEnabledWhenATrackedEffortIsMoved(self):
        self.task.addEffort(self.effort1)
        self.taskList.append(self.task2)
        self.effort1.setTask(self.task2)
        if not self.effortStop.enabled():
            print self.effortStop.log
        self.failUnless(self.effortStop.enabled())
        
    # Tests of EffortStop.doCommand()

    def testDoCommandStopsTrackedEffort(self):
        self.task.addEffort(self.effort1)
        self.effortStop.doCommand()
        self.failIf(self.effort1.isBeingTracked())
        
    def testDoCommandStopsAllTrackedEffort(self):
        self.task.addEffort(self.effort1)
        self.task.addEffort(self.effort2)
        self.effortStop.doCommand()
        self.failIf(self.task.isBeingTracked())
