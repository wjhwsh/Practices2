//
//  TaskTableView.m
//  Task Coach
//
//  Created by Jérôme Laheurte on 03/04/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "TaskTableView.h"
#import "Task_CoachAppDelegate.h"
#import "CDDomainObject+Addons.h"
#import "SmartAlertView.h"
#import "Configuration.h"
#import "CDTask+Addons.h"
#import "String+Utils.h"
#import "TaskHeaderViewFactory.h"
#import "TaskCellFactory.h"
#import "TaskDetailsCell.h"
#import "TaskView.h"
#import "DateUtils.h"
#import "NSDateUtils.h"
#import "i18n.h"

@implementation TaskTableView

@synthesize detailsTask;

- (void)dealloc
{
    [self viewDidUnload];
    [detailsTask release];
    [scrollTo release];

    [super dealloc];
}

- (void)reload
{
    if (resultsCtrl)
    {
        [resultsCtrl release];
    }
    
    NSFetchRequest *req = [[NSFetchRequest alloc] init];
    [req setEntity:[NSEntityDescription entityForName:@"CDTask" inManagedObjectContext:getManagedObjectContext()]];
    [req setPredicate:[NSPredicate predicateWithFormat:@"status != %d AND list=%@", STATUS_DELETED, [Configuration instance].currentList]];
    
    NSMutableArray *sorting = [[NSMutableArray alloc] initWithCapacity:3];
    NSSortDescriptor *des;
    
    des = [[NSSortDescriptor alloc] initWithKey:[Configuration instance].groupingName ascending:![Configuration instance].revertGrouping];
    [sorting addObject:des];
    [des release];
    
    if ([Configuration instance].grouping != GROUPING_START)
    {
        des = [[NSSortDescriptor alloc] initWithKey:@"startDate" ascending:YES];
        [sorting addObject:des];
        [des release];
    }
    
    des = [[NSSortDescriptor alloc] initWithKey:@"name" ascending:YES];
    [sorting addObject:des];
    [des release];
    
    [req setSortDescriptors:sorting];
    [sorting release];
    
    resultsCtrl = [[NSFetchedResultsController alloc] initWithFetchRequest:req managedObjectContext:getManagedObjectContext() sectionNameKeyPath:[Configuration instance].groupingName cacheName:nil];
    [req release];
    
    NSError *error;
    if (![resultsCtrl performFetch:&error])
    {
        SmartAlertView *alert = [[SmartAlertView alloc] initWithTitle:_("Error") message:[NSString stringWithFormat:_("Could not fetch tasks: %@"), [error localizedDescription]] cancelButtonTitle:_("OK") cancelAction:^(void) {
            // Nothing
        }];
        [alert show];
        [alert release];
    }

    resultsCtrl.delegate = self;
}

- (void)addTask
{
    CDTask *task = [NSEntityDescription insertNewObjectForEntityForName:@"CDTask" inManagedObjectContext:getManagedObjectContext()];
    
    if (detailsTask)
    {
        [self.tableView reloadRowsAtIndexPaths:[NSArray arrayWithObject:[resultsCtrl indexPathForObject:detailsTask]] withRowAnimation:UITableViewRowAnimationFade];
        [detailsTask release];
    }
    
    editSubject = YES;

    task.name = _("New task");
    task.longDescription = @"";
    task.startDate = [NSDate date];
    task.list = [Configuration instance].currentList;
    task.creationDate = [NSDate date];
    [task computeDateStatus];
    detailsTask = task;
    [task save];

    [self.tableView scrollToRowAtIndexPath:[resultsCtrl indexPathForObject:task] atScrollPosition:UITableViewScrollPositionTop animated:YES];
    [self.tableView setScrollEnabled:NO];
}

- (void)doneEditing
{
    NSIndexPath *path = [resultsCtrl indexPathForObject:detailsTask];
    [detailsTask release];
    detailsTask = nil;
    [detailsCell release];
    detailsCell = nil;

    [self.tableView reloadData];
    [self.tableView setScrollEnabled:YES];
    [self.tableView scrollToRowAtIndexPath:path atScrollPosition:UITableViewScrollPositionMiddle animated:YES];
    [taskView enableUpdates];
    [groupingButton setEnabled:YES];
    [addButton setEnabled:YES];
}

#pragma mark - View lifecycle

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self reload];
}

- (void)viewDidUnload
{
    [super viewDidUnload];

    [resultsCtrl release];
    resultsCtrl = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return YES;
}

- (void)viewDidAppear:(BOOL)animated
{

    [super viewDidAppear:animated];
}

- (void)viewWillDisappear:(BOOL)animated
{
    [super viewWillDisappear:animated];
}

- (void)refresh
{
    NSFetchRequest *req = [[NSFetchRequest alloc] init];
    [req setEntity:[NSEntityDescription entityForName:@"CDTask" inManagedObjectContext:getManagedObjectContext()]];
    [req setPredicate:[NSPredicate predicateWithFormat:@"ANY efforts.ended = NULL"]];
    NSError *error;
    NSArray *tasks = [getManagedObjectContext() executeFetchRequest:req error:&error];
    [req release];
    
    if (tasks)
    {
        NSMutableArray *paths = [[NSMutableArray alloc] init];

        for (CDTask *task in tasks)
        {
            NSIndexPath *indexPath = [resultsCtrl indexPathForObject:task];
            if (indexPath)
            {
                [paths addObject:indexPath];
            }
        }

        [self.tableView reloadRowsAtIndexPaths:paths withRowAnimation:UITableViewRowAnimationNone];
    }
    else
    {
        NSLog(@"Could not fetch tracked tasks: %@", [error localizedDescription]);
    }
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return [[resultsCtrl sections] count];
}

- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section
{
    if (detailsTask)
        return nil;

    id <NSFetchedResultsSectionInfo> info = [[resultsCtrl sections] objectAtIndex:section];

    switch ([Configuration instance].grouping)
    {
        case GROUPING_PRIORITY:
            return [info name];
        default:
        {
            struct tm cdate;
            (void)strptime([[info name] UTF8String], "%Y-%m-%d %H:%M:%S %z", &cdate);
            NSDate *date = [NSDate dateWithTimeIntervalSince1970:mktime(&cdate)];

            return [[UserTimeUtils instance] stringFromDate:date];
        }
    }

    return nil;
}

- (UIView *)tableView:(UITableView *)tableView viewForHeaderInSection:(NSInteger)section
{
    if (detailsTask)
        return nil;

    if ([Configuration instance].grouping == GROUPING_STATUS)
    {
        TaskHeaderView *view = [[TaskHeaderViewFactory instance] create];
        [view setStyle:[[[[resultsCtrl sections] objectAtIndex:section] name] intValue]];
        return view;
    }

    return nil;
}

- (CGFloat)tableView:(UITableView *)tableView heightForHeaderInSection:(NSInteger)section
{
    return 41;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    if ([indexPath isEqual:[resultsCtrl indexPathForObject:detailsTask]])
        return 432;
    return 44;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    id <NSFetchedResultsSectionInfo> info = [[resultsCtrl sections] objectAtIndex:section];
    return [info numberOfObjects];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    if ([indexPath isEqual:[resultsCtrl indexPathForObject:detailsTask]])
    {
        if (!detailsCell)
        {
            detailsCell = [[[TaskCellFactory instance] createDetails] retain];

            CDTask *task = [resultsCtrl objectAtIndexPath:indexPath];
            [detailsCell setTask:task callback:^(id sender) {
                [self doneEditing];
            }];
            
            if (editSubject)
            {
                // XXXFIXME: If the cell is at the bottom of the view,
                // the keyboard hides it...
                
                editSubject = NO;
                [detailsCell editSubject];
            }
        }

        return detailsCell;
    }
    else
    {
        static NSString *CellIdentifier = @"TaskCell";
    
        TaskCell *cell = (TaskCell *)[tableView dequeueReusableCellWithIdentifier:CellIdentifier];
        if (cell == nil)
        {
            cell = [[TaskCellFactory instance] create];
        }

        CDTask *task = [resultsCtrl objectAtIndexPath:indexPath];
        [cell setTask:task];
    
        return cell;
    }
}

/*
// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the specified item to be editable.
    return YES;
}
*/

/*
// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        // Delete the row from the data source
        [tableView deleteRowsAtIndexPaths:[NSArray arrayWithObject:indexPath] withRowAnimation:UITableViewRowAnimationFade];
    }   
    else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }   
}
*/

/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath
{
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

#pragma mark - Table view delegate

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    if ([indexPath isEqual:[resultsCtrl indexPathForObject:detailsTask]])
        return;

    NSMutableArray *paths = [[NSMutableArray alloc] initWithCapacity:2];

    if (detailsTask)
    {
        [paths addObject:[resultsCtrl indexPathForObject:detailsTask]];
        [detailsTask release];
    }

    detailsTask = [[resultsCtrl objectAtIndexPath:indexPath] retain];
    [paths addObject:indexPath];

    [self.tableView reloadRowsAtIndexPaths:paths withRowAnimation:UITableViewRowAnimationFade];
    [paths release];

    [self.tableView scrollToRowAtIndexPath:indexPath atScrollPosition:UITableViewScrollPositionTop animated:YES];
    [self.tableView setScrollEnabled:NO];

    [taskView disableUpdates];

    [groupingButton setEnabled:NO];
    [addButton setEnabled:NO];
}

#pragma mark - Fetched results controller delegate

- (void)controllerWillChangeContent:(NSFetchedResultsController *)controller
{
    [self.tableView beginUpdates];
}

- (void)controller:(NSFetchedResultsController *)controller didChangeSection:(id <NSFetchedResultsSectionInfo>)sectionInfo
           atIndex:(NSUInteger)sectionIndex forChangeType:(NSFetchedResultsChangeType)type
{
    if (detailsCell)
        return;

    switch(type) {
        case NSFetchedResultsChangeInsert:
            [self.tableView insertSections:[NSIndexSet indexSetWithIndex:sectionIndex]
                          withRowAnimation:UITableViewRowAnimationFade];
            break;
            
        case NSFetchedResultsChangeDelete:
            [self.tableView deleteSections:[NSIndexSet indexSetWithIndex:sectionIndex]
                          withRowAnimation:UITableViewRowAnimationFade];
            break;
    }
}

- (void)controller:(NSFetchedResultsController *)controller didChangeObject:(id)anObject
       atIndexPath:(NSIndexPath *)indexPath forChangeType:(NSFetchedResultsChangeType)type
      newIndexPath:(NSIndexPath *)newIndexPath
{
    UITableView *tableView = self.tableView;

    if (detailsCell)
        return;

    switch(type) {
            
        case NSFetchedResultsChangeInsert:
            [tableView insertRowsAtIndexPaths:[NSArray arrayWithObject:newIndexPath]
                             withRowAnimation:UITableViewRowAnimationFade];
            break;
            
        case NSFetchedResultsChangeDelete:
            [tableView deleteRowsAtIndexPaths:[NSArray arrayWithObject:indexPath]
                             withRowAnimation:UITableViewRowAnimationFade];
            break;
            
        case NSFetchedResultsChangeUpdate:
            [tableView reloadRowsAtIndexPaths:[NSArray arrayWithObject:indexPath] withRowAnimation:UITableViewRowAnimationFade];
            break;
            
        case NSFetchedResultsChangeMove:
            [tableView deleteRowsAtIndexPaths:[NSArray arrayWithObject:indexPath]
                             withRowAnimation:UITableViewRowAnimationRight];
            [tableView insertRowsAtIndexPaths:[NSArray arrayWithObject:newIndexPath]
                             withRowAnimation:UITableViewRowAnimationRight];
            if ([newIndexPath isEqual:[resultsCtrl indexPathForObject:detailsTask]])
            {
                scrollTo = [newIndexPath copy];
            }
            break;
    }
}

- (void)controllerDidChangeContent:(NSFetchedResultsController *)controller
{
    [self.tableView endUpdates];

    if (scrollTo)
    {
        [self.tableView scrollToRowAtIndexPath:scrollTo atScrollPosition:UITableViewScrollPositionTop animated:YES];
        [scrollTo release];
        scrollTo = nil;
    }
}

@end
