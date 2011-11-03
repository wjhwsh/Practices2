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

from unittests import asserts
from CommandTestCase import CommandTestCase
from taskcoachlib import command, patterns, config
from taskcoachlib.domain import task, effort, date, category, attachment


class TaskCommandTestCase(CommandTestCase, asserts.Mixin):
    def setUp(self):
        super(TaskCommandTestCase, self).setUp()
        task.Task.settings = config.Settings(load=False)
        self.list = self.taskList = task.TaskList()
        self.categories = category.CategoryList()
        self.category = category.Category('cat')
        self.categories.append(self.category)
        self.task1 = task.Task('task1', startDateTime=date.Now())
        self.task2 = task.Task('task2', startDateTime=date.Now())
        self.taskList.append(self.task1)
        self.originalList = [self.task1]
        
    def tearDown(self):
        super(TaskCommandTestCase, self).tearDown()
        command.Clipboard().clear()

    def delete(self, items=None, shadow=False):
        if items == 'all':
            items = list(self.list)
        command.DeleteTaskCommand(self.list, items or [], shadow=shadow).do()
 
    def paste(self, items=None): # pylint: disable-msg=W0221
        if items:
            command.PasteAsSubItemCommand(self.taskList, items).do()
        else:
            super(TaskCommandTestCase, self).paste()

    def copy(self, items=None):
        command.CopyCommand(self.list, items or []).do()
        
    def markCompleted(self, tasks=None):
        command.MarkCompletedCommand(self.taskList, tasks or []).do()

    def newSubTask(self, tasks=None, markCompleted=False):
        tasks = tasks or []
        newSubTask = command.NewSubTaskCommand(self.taskList, tasks)
        if markCompleted:
            for subtask in newSubTask.items:
                subtask.setCompletionDateTime()
        newSubTask.do()

    def dragAndDrop(self, dropTarget, tasks=None):
        command.DragAndDropTaskCommand(self.taskList, tasks or [], 
                                       drop=dropTarget).do()
        
    def editStart(self, newStartDateTime, tasks=[]):
        command.EditStartDateTimeCommand(self.taskList, tasks or [],
                                         datetime=newStartDateTime).do()
        

class CommandWithChildrenTestCase(TaskCommandTestCase):
    def setUp(self):
        super(CommandWithChildrenTestCase, self).setUp()
        self.parent = task.Task('parent')
        self.child = task.Task('child')
        self.parent.addChild(self.child)
        self.child2 = task.Task('child2')
        self.parent.addChild(self.child2)
        self.grandchild = task.Task('grandchild')
        self.child.addChild(self.grandchild)
        self.originalList.extend([self.parent, self.child, self.child2, self.grandchild])
        self.taskList.append(self.parent)
        

class CommandWithEffortTestCase(TaskCommandTestCase):
    def setUp(self):
        super(CommandWithEffortTestCase, self).setUp()
        self.list = self.effortList = effort.EffortList(self.taskList)
        self.effort1 = effort.Effort(self.task1)
        self.task1.addEffort(self.effort1)
        self.effort2 = effort.Effort(self.task2, 
            date.DateTime(2004,1,1), date.DateTime(2004,1,2))
        self.task2.addEffort(self.effort2)
        self.taskList.append(self.task2)
        self.originalEffortList = [self.effort1, self.effort2]


class DeleteCommandWithTasksTest(TaskCommandTestCase):
    def testDeleteAllTasks(self):
        self.taskList.append(self.task2)
        self.delete('all')
        self.assertDoUndoRedo(self.assertEmptyTaskList, 
            lambda: self.assertTaskList([self.task1, self.task2]))

    def testDeleteOneTask(self):
        self.taskList.append(self.task2)
        self.delete([self.task1])
        self.assertDoUndoRedo(lambda: self.assertTaskList([self.task2]),
            lambda: self.assertTaskList([self.task1, self.task2]))

    def testDeleteEmptyList(self):
        self.taskList.remove(self.task1)
        self.delete('all')
        self.assertDoUndoRedo(self.assertEmptyTaskList)

    def testDeleteEmptyList_NoCommandHistory(self):
        self.taskList.remove(self.task1)
        self.delete('all')
        self.assertDoUndoRedo(lambda: self.assertHistoryAndFuture([], []))

    def testDelete(self):
        self.delete('all')
        self.assertDoUndoRedo(self.assertEmptyTaskList,
            lambda: self.assertTaskList(self.originalList))
        
    def testDeleteTaskWithCategory(self):
        self.category.addCategorizable(self.task1)
        self.task1.addCategory(self.category)
        self.delete('all')
        self.assertDoUndoRedo(lambda: self.failIf(self.category.categorizables()), 
            lambda: self.assertEqual(set([self.task1]), self.category.categorizables()))
        
    def testDeleteTaskWithTwoCategories(self):
        cat1 = category.Category('category 1')
        cat2 = category.Category('category 2')
        self.categories.extend([cat1, cat2])
        for cat in cat1, cat2:
            cat.addCategorizable(self.task1)
            self.task1.addCategory(cat)
        self.delete('all')
        self.assertDoUndoRedo(lambda: self.failIf(cat1.categorizables() or cat2.categorizables()), 
            lambda: self.failUnless(set([self.task1]) == cat1.categorizables() == cat2.categorizables()))
        
    def testDeleteTaskThatIsPrerequisite(self):
        self.task2.addPrerequisites([self.task1])
        self.task1.addDependencies([self.task2])
        self.taskList.append(self.task2)
        self.delete([self.task1])
        self.assertDoUndoRedo(lambda: self.failIf(self.task2.prerequisites()),
                              lambda: self.failUnless(self.task2.prerequisites()))

    def testDeleteTaskThatIsDependency(self):
        self.task2.addPrerequisites([self.task1])
        self.taskList.append(self.task2)
        self.delete([self.task2])
        self.assertDoUndoRedo(lambda: self.failIf(self.task1.dependencies()),
                              lambda: self.failUnless(self.task1.dependencies()))


class DeleteCommandWithTasksWithChildrenTest(CommandWithChildrenTestCase):
    def assertDeleteWorks(self):
        self.assertDoUndoRedo(self.assertParentAndAllChildrenDeleted,
            self.assertTaskListUnchanged)

    def assertParentAndAllChildrenDeleted(self):
        self.assertTaskList([self.task1])

    def assertTaskListUnchanged(self):
        self.assertTaskList(self.originalList)
        self.failUnlessParentAndChild(self.parent, self.child)
        self.failUnlessParentAndChild(self.child, self.grandchild)

    def assertShadowed(self, *shadowedTasks):
        for shadowedTask in shadowedTasks:
            self.failUnless(shadowedTask.isDeleted())
        
    def testDeleteParent(self):
        self.delete([self.parent])
        self.assertDeleteWorks()
        
    def testDeleteParentWhileShadowing(self):
        self.delete([self.parent], shadow=True)
        self.assertShadowed(self.parent, *self.parent.children())
        
    def testDeleteParentAndChild(self):
        self.delete([self.parent, self.child])
        self.assertDeleteWorks()

    def testDeleteParentAndGrandchild(self):
        self.delete([self.parent, self.grandchild])
        self.assertDeleteWorks()

    def testDeleteLastNotCompletedChildMarksParentAsCompleted(self):
        self.markCompleted([self.child2])
        self.delete([self.child])
        self.assertDoUndoRedo(
            lambda: self.failUnless(self.parent.completed()), 
            lambda: self.failIf(self.parent.completed()))
        
    def testDeleteParentAndChildWhenChildBelongsToCategory(self):
        self.category.addCategorizable(self.child)
        self.child.addCategory(self.category)
        self.delete([self.parent])
        self.assertDoUndoRedo(lambda: self.failIf(self.category.categorizables()), 
            lambda: self.assertEqual(set([self.child]), self.category.categorizables()))

    def testDeleteParentAndChildWhenParentAndChildBelongToDifferentCategories(self):
        cat1 = category.Category('category 1')
        cat2 = category.Category('category 2')
        self.categories.extend([cat1, cat2])
        cat1.addCategorizable(self.child)
        self.child.addCategory(cat1)
        cat2.addCategorizable(self.parent)
        self.parent.addCategory(cat2)
        self.delete([self.parent])
        self.assertDoUndoRedo(lambda: self.failIf(cat1.categorizables() or cat2.categorizables()), 
            lambda: self.failUnless(set([self.child]) == cat1.categorizables() and \
                                    set([self.parent]) == cat2.categorizables()))

    def testDeleteParentAndChildWhenParentAndChildBelongToSameCategory(self):
        for eachTask in self.parent, self.child:
            self.category.addCategorizable(eachTask)
            eachTask.addCategory(self.category)
        self.delete([self.parent])
        self.assertDoUndoRedo( \
            lambda: self.failIf(self.category.categorizables()), 
            lambda: self.assertEqualLists([self.parent, self.child], 
                                          self.category.categorizables()))


class DeleteCommandWithTasksWithEffortTest(CommandWithEffortTestCase):
    def testDeleteActiveTask(self):
        self.list = self.taskList
        self.delete([self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(1, len(self.effortList)),
            lambda: self.assertEqual(2, len(self.effortList)))


class NewTaskCommandTest(TaskCommandTestCase):
    def new(self, **kwargs):
        newTaskCommand = command.NewTaskCommand(self.taskList, **kwargs)
        newTask = newTaskCommand.items[0]
        newTaskCommand.do()
        return newTask
    
    def testNewTask(self):
        newTask = self.new()
        self.assertDoUndoRedo(
            lambda: self.assertTaskList([self.task1, newTask]),
            lambda: self.assertTaskList(self.originalList))
        
    def testNewTaskWithCategory(self):
        cat = category.Category('cat')
        newTask = self.new(categories=[cat])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(set([cat]), newTask.categories()),
            lambda: self.assertTaskList(self.originalList))

    def testNewTaskWithCategory_AddsTaskToCategory(self):
        cat = category.Category('cat')
        newTask = self.new(categories=[cat])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(set([newTask]), cat.categorizables()),
            lambda: self.failIf(cat.categorizables()))

    def testNewTaskWithPrerequisite(self):
        newTask = self.new(prerequisites=[self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(set([self.task1]), newTask.prerequisites()),
            lambda: self.assertTaskList(self.originalList))
        
    def testNewTaskWithPrerequisite_AddsDependency(self):
        newTask = self.new(prerequisites=[self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(set([newTask]), self.task1.dependencies()),
            lambda: self.failIf(self.task1.dependencies()))

    def testNewTaskWithDependency(self):
        newTask = self.new(dependencies=[self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(set([self.task1]), newTask.dependencies()),
            lambda: self.assertTaskList(self.originalList))

    def testNewTaskWithDependency_AddsPrerequisite(self):
        newTask = self.new(dependencies=[self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(set([newTask]), self.task1.prerequisites()),
            lambda: self.failIf(self.task1.prerequisites()))
        
    def testNewTaskWithAttachment(self):
        att = attachment.FileAttachment('filename')
        newTask = self.new(attachments=[att])
        self.assertDoUndoRedo(
            lambda: self.assertEqual([att], newTask.attachments()),
            lambda: self.assertTaskList(self.originalList))
        
    def testNewTaskWithKeywords(self):
        dateTime = date.DateTime(2042, 2, 3)
        newTask = self.new(startDateTime=dateTime)
        self.assertEqual(dateTime, newTask.startDateTime())


class NewSubTaskCommandTest(TaskCommandTestCase):
    def testNewSubTask_WithoutSelection(self):
        self.newSubTask()
        self.assertDoUndoRedo(lambda: self.assertTaskList(self.originalList))

    def testNewSubTask(self):
        self.newSubTask([self.task1])
        newSubTask = self.task1.children()[0]
        self.assertDoUndoRedo(lambda: self.assertNewSubTask(newSubTask),
            lambda: self.assertTaskList(self.originalList))

    def assertNewSubTask(self, newSubTask):
        self.assertEqual(len(self.originalList)+1, len(self.taskList))
        self.assertEqualLists([newSubTask], self.task1.children())

    def testNewSubTask_MarksParentAsNotCompleted(self):
        self.markCompleted([self.task1])
        self.newSubTask([self.task1])
        self.assertDoUndoRedo(lambda: self.failIf(self.task1.completed()),
            lambda: self.failUnless(self.task1.completed()))

    def testNewSubTask_MarksGrandParentAsNotCompleted(self):
        self.newSubTask([self.task1])
        self.markCompleted([self.task1])
        self.newSubTask([self.task1.children()[0]])
        self.assertDoUndoRedo(lambda: self.failIf(self.task1.completed()),
            lambda: self.failUnless(self.task1.completed()))

    def testNewCompletedSubTask(self):
        self.newSubTask([self.task1], markCompleted=True)
        self.assertDoUndoRedo(lambda: self.failUnless(self.task1.completed()),
            lambda: self.failIf(self.task1.completed()))


class MarkCompletedCommandTest(CommandWithChildrenTestCase):
    def testMarkCompleted(self):
        self.markCompleted([self.task1])
        self.assertDoUndoRedo(
            lambda: self.failUnless(self.task1.completed()),
            lambda: self.failIf(self.task1.completed()))

    def testMarkCompleted_TaskAlreadyCompleted(self):
        self.task1.setCompletionDateTime()
        self.markCompleted([self.task1])
        self.assertDoUndoRedo(
            lambda: self.failIf(self.task1.completed()),
            lambda: self.failUnless(self.task1.completed()))

    def testMarkCompletedParent(self):
        self.markCompleted([self.parent])
        self.assertDoUndoRedo(lambda: self.failUnless(self.child.completed()
            and self.child2.completed() and self.grandchild.completed()),
            lambda: self.failIf(self.child.completed() or
            self.child2.completed() or self.grandchild.completed()))

    def testMarkCompletedParent_WhenChildAlreadyCompleted(self):
        self.markCompleted([self.child])
        self.markCompleted([self.parent])
        self.assertDoUndoRedo(lambda: self.failUnless(self.child.completed()))

    def testMarkCompletedGrandChild(self):
        self.markCompleted([self.grandchild])
        self.assertDoUndoRedo(
            lambda: self.failUnless(self.child.completed() and 
                not self.parent.completed()), 
            lambda: self.failIf(self.child.completed() or 
                self.parent.completed()))

    def testMarkCompletedStopsEffortTracking(self):
        self.task1.addEffort(effort.Effort(self.task1))
        self.markCompleted([self.task1])
        self.assertDoUndoRedo(lambda: self.failIf(self.task1.isBeingTracked()), 
            lambda: self.failUnless(self.task1.isBeingTracked()))
            
    def testMarkCompletedChildDoesNotStopEffortTrackingOfParent(self):
        self.parent.addEffort(effort.Effort(self.parent))
        self.markCompleted([self.child])
        self.assertDoUndoRedo(lambda: self.failUnless(self.parent.isBeingTracked()))
        
    def testMarkRecurringTaskCompleted_CompletionDateIsNotSet(self):
        self.task1.setRecurrence(date.Recurrence('weekly'))
        self.markCompleted([self.task1])
        self.assertDoUndoRedo(lambda: self.failIf(self.task1.completed()))

    def testMarkRecurringTaskCompleted_StartDateIsIncreased(self):
        self.task1.setRecurrence(date.Recurrence('weekly'))
        startDateTime = self.task1.startDateTime()
        newStartDateTime = startDateTime + date.TimeDelta(days=7)
        self.markCompleted([self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(newStartDateTime, self.task1.startDateTime()),
            lambda: self.assertEqual(startDateTime, self.task1.startDateTime()))

    def testMarkRecurringTaskCompleted_DueDateIsIncreased(self):
        self.task1.setRecurrence(date.Recurrence('weekly'))
        tomorrow = date.Now() + date.oneDay
        self.task1.setDueDateTime(tomorrow)
        newDueDate = tomorrow + date.TimeDelta(days=7)
        self.markCompleted([self.task1])
        self.assertDoUndoRedo(
            lambda: self.assertEqual(newDueDate, self.task1.dueDateTime()),
            lambda: self.assertEqual(tomorrow, self.task1.dueDateTime()))
        
    def testMarkParentWithRecurringChildCompleted_RemovesChildRecurrence(self):
        self.child.setRecurrence(date.Recurrence('daily'))
        self.markCompleted([self.parent])
        self.assertDoUndoRedo(
            lambda: self.failIf(self.child.recurrence()),
            lambda: self.assertEqual(date.Recurrence('daily'), self.child.recurrence()))

    def testMarkParentWithRecurringChildCompleted_MakesChildCompleted(self):
        self.child.setRecurrence(date.Recurrence('daily'))
        self.markCompleted([self.parent])
        self.assertDoUndoRedo(
            lambda: self.failUnless(self.child.completed()),
            lambda: self.failIf(self.child.completed()))
        
        
class DragAndDropTaskCommandTest(CommandWithChildrenTestCase):
    def testCannotDropOnParent(self):
        self.dragAndDrop([self.parent], [self.child])
        self.failIf(patterns.CommandHistory().hasHistory())
        
    def testCannotDropOnChild(self):
        self.dragAndDrop([self.child], [self.parent])
        self.failIf(patterns.CommandHistory().hasHistory())
        
    def testCannotDropOnGrandchild(self):
        self.dragAndDrop([self.grandchild], [self.parent])
        self.failIf(patterns.CommandHistory().hasHistory())

    def testDropAsRootTask(self):
        self.dragAndDrop([], [self.grandchild])
        self.assertDoUndoRedo(lambda: self.assertEqual(None, 
            self.grandchild.parent()), lambda:
            self.assertEqual(self.child, self.grandchild.parent()))
        

class PriorityCommandTestCase(TaskCommandTestCase):
    def setUp(self):
        super(PriorityCommandTestCase, self).setUp()
        self.taskList.append(self.task2)

    def assertDoUndoRedo(self, priority1do, priority2do, priority1undo, priority2undo): # pylint: disable-msg=W0221
        super(PriorityCommandTestCase, self).assertDoUndoRedo(
            lambda: self.failUnless(priority1do == self.task1.priority() and
                    priority2do == self.task2.priority()),
            lambda: self.failUnless(priority1undo == self.task1.priority() and
                    priority2undo == self.task2.priority()))

        
class MaxPriorityCommandTest(PriorityCommandTestCase):
    def maxPriority(self, tasks=None):
        command.MaxPriorityCommand(self.taskList, tasks or []).do()        
        
    def testEmptySelection(self):
        self.maxPriority()
        self.assertDoUndoRedo(0, 0, 0, 0)
        
    def testOneTaskWhenBothTasksHaveSamePriority(self):
        self.maxPriority([self.task1])
        self.assertDoUndoRedo(1, 0, 0, 0)
        
    def testBothTasksWhenBothTasksHaveSamePriority(self):
        self.maxPriority([self.task1, self.task2])
        self.assertDoUndoRedo(1, 1, 0, 0)
        
    def testMakeLowestPriorityTheMaxPriority(self):
        self.task2.setPriority(2)
        self.maxPriority([self.task1])
        self.assertDoUndoRedo(3, 2, 0, 2)


class MinPriorityCommandTest(PriorityCommandTestCase):        
    def minPriority(self, tasks=None):
        command.MinPriorityCommand(self.taskList, tasks or []).do()        

    def testEmptySelection(self):
        self.minPriority()
        self.assertDoUndoRedo(0, 0, 0, 0)
        
    def testOneTaskWhenBothTasksHaveSamePriority(self):
        self.minPriority([self.task1])
        self.assertDoUndoRedo(-1, 0, 0, 0)
        
    def testBothTasksWhenBothTasksHaveSamePriority(self):
        self.minPriority([self.task1, self.task2])
        self.assertDoUndoRedo(-1, -1, 0, 0)
        
    def testMakeLowestPriorityTheMaxPriority(self):
        self.task2.setPriority(-2)
        self.minPriority([self.task1])
        self.assertDoUndoRedo(-3, -2, 0, -2)


class IncreasePriorityCommandTest(PriorityCommandTestCase):
    def incPriority(self, tasks=None):
        command.IncPriorityCommand(self.taskList, tasks or []).do()
        
    def testEmptySelection(self):
        self.incPriority()
        self.assertDoUndoRedo(0, 0, 0, 0)
        
    def testOneTaskWhenBothTasksHaveSamePriority(self):
        self.incPriority([self.task1])
        self.assertDoUndoRedo(1, 0, 0, 0)
        
    def testBothTasksWhenBothTasksHaveSamePriority(self):
        self.incPriority([self.task1, self.task2])
        self.assertDoUndoRedo(1, 1, 0, 0)
        
    def testIncLowestPriority(self):
        self.task2.setPriority(-2)
        self.incPriority([self.task2])
        self.assertDoUndoRedo(0, -1, 0, -2)
    

class DecreasePriorityCommandTest(PriorityCommandTestCase):
    def decPriority(self, tasks=None):
        command.DecPriorityCommand(self.taskList, tasks or []).do()
        
    def testEmptySelection(self):
        self.decPriority()
        self.assertDoUndoRedo(0, 0, 0, 0)
        
    def testOneTaskWhenBothTasksHaveSamePriority(self):
        self.decPriority([self.task1])
        self.assertDoUndoRedo(-1, 0, 0, 0)
        
    def testBothTasksWhenBothTasksHaveSamePriority(self):
        self.decPriority([self.task1, self.task2])
        self.assertDoUndoRedo(-1, -1, 0, 0)
        
    def testDecLowestPriority(self):
        self.task2.setPriority(-2)
        self.decPriority([self.task2])
        self.assertDoUndoRedo(0, -3, 0, -2)
        

class AddNoteCommandTest(TaskCommandTestCase):
    def addNote(self, tasks=None):
        command.AddNoteCommand(self.taskList, tasks or []).do()
    
    # pylint: disable-msg=E1101
    
    def testEmptySelection(self):
        self.addNote()
        self.assertDoUndoRedo(lambda: self.failIf(self.task1.notes()))
        
    def testAddNote(self):
        self.addNote([self.task1])
        self.assertDoUndoRedo(lambda: self.failUnless(self.task1.notes()),
            lambda: self.failIf(self.task1.notes()))
            
    def testAddNoteToMultipleTasksAtOnce(self):
        self.addNote([self.task1, self.task2])
        self.assertDoUndoRedo(\
            lambda: self.failIf(self.task1.notes()[0] == self.task2.notes()[0]),
            lambda: self.failIf(self.task1.notes() or self.task2.notes()))
    

class EditStartDateCommandTest(TaskCommandTestCase):
    def testSetStartDateToTomorrow(self):
        previousStart = self.task1.startDateTime()
        newStart = date.Now() + date.TimeDelta(hours=1)
        self.editStart(newStart, [self.task1])
        self.assertDoUndoRedo(\
            lambda: self.assertEqual(newStart, self.task1.startDateTime()),
            lambda: self.assertEqual(previousStart, self.task1.startDateTime()))
        
    def testPushingBackStartDatePushesBackDueDate(self):
        self.task1.setDueDateTime(date.Now() + date.TimeDelta(hours=2)) 
        previousStart = self.task1.startDateTime()
        previousDue = self.task1.dueDateTime()
        pushBack = date.TimeDelta(hours=1)
        newStart = previousStart + pushBack
        expectedDue = previousDue + pushBack
        self.editStart(newStart, [self.task1])
        self.assertDoUndoRedo(\
            lambda: self.assertEqual(expectedDue, self.task1.dueDateTime()),
            lambda: self.assertEqual(previousDue, self.task1.dueDateTime()))
        
    def testMissingDueDateIsNotPushedBack(self):
        previousStart = self.task1.startDateTime()
        pushBack = date.TimeDelta(hours=1)
        newStart = previousStart + pushBack
        expectedDue = date.DateTime()
        self.editStart(newStart, [self.task1])
        self.assertDoUndoRedo(\
            lambda: self.assertEqual(expectedDue, self.task1.dueDateTime()))
        
    def testDueDateIsNotPushedBackWhenStartDateIsMissing(self):
        self.task1.setStartDateTime(date.DateTime())
        self.task1.setDueDateTime(date.Now() + date.TimeDelta(hours=2))
        pushBack = date.TimeDelta(hours=1)
        newStart = date.Now() + pushBack
        expectedDue = self.task1.dueDateTime()
        self.editStart(newStart, [self.task1])
        self.assertDoUndoRedo(\
            lambda: self.assertEqual(expectedDue, self.task1.dueDateTime()))