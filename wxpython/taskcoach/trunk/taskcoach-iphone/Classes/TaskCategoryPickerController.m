//
//  TaskCategoryPickerController.m
//  TaskCoach
//
//  Created by Jérôme Laheurte on 02/08/09.
//  Copyright 2009 Jérôme Laheurte. See COPYING for details.
//

#import "TaskCoachAppDelegate.h"

#import "TaskCategoryPickerController.h"
#import "BadgedCell.h"

#import "CDDomainObject+Addons.h"
#import "CDTask.h"
#import "CDCategory.h"
#import "LogUtils.h"

#import "i18n.h"

@implementation TaskCategoryPickerController

#pragma mark Object lifetime

- initWithTask:(CDTask *)task
{
	if ((self = [super initWithNibName:@"TaskCategoryPicker" bundle:[NSBundle mainBundle]]))
	{
		myTask = [task retain];
	}
	
	return self;
}

- (void)dealloc
{
	[myTask release];
	
	[super dealloc];
}

- (void)setTask:(CDTask *)task
{
	[myTask release];
	myTask = [task retain];
	[self loadCategories];
	[self.tableView reloadData];
}

#pragma mark Domain methods

- (void)fillCell:(BadgedCell *)cell forCategory:(CDCategory *)category
{
	[super fillCell:cell forCategory:category];

	if ([[myTask categories] containsObject:category])
	{
		[cell setChecked:YES];
		[cell setNeedsDisplay];
	}
}

#pragma mark Table view methods

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
	CDCategory *category = [categories objectAtIndex:indexPath.row];
	BadgedCell *cell = (BadgedCell *)[self.tableView cellForRowAtIndexPath:indexPath];

	if ([[myTask categories] containsObject:category])
	{
		JLDEBUG("Category \"%s\" deselected", [category.name UTF8String]);

		[myTask removeCategoriesObject:category];
		[cell setChecked:NO];
	}
	else
	{
		JLDEBUG("Category \"%s\" selected", [category.name UTF8String]);

		[myTask addCategoriesObject:category];
		[cell setChecked:YES];
	}

	[cell setNeedsDisplay];

	[myTask markDirty];
	[myTask save];

	[self.tableView deselectRowAtIndexPath:indexPath animated:YES];
}

@end
