//
//  BaseCategoryViewController.m
//  TaskCoach
//
//  Created by Jérôme Laheurte on 02/08/09.
//  Copyright 2009 Jérôme Laheurte. See COPYING for details.
//

#import "TaskCoachAppDelegate.h"
#import "BaseCategoryViewController.h"
#import "Configuration.h"
#import "BadgedCell.h"
#import "CellFactory.h"
#import "LogUtils.h"

#import "CDCategory.h"
#import "CDDomainObject+Addons.h"

static NSInteger compareCategories(id a, id b, void *ctx)
{
	return [[a name] localizedCaseInsensitiveCompare:[b name]];
}

static NSMutableArray *expandChildren(CDCategory *category, NSMutableDictionary *indentations, NSInteger indent)
{
	NSMutableArray *allChildren = [[[NSMutableArray alloc] init] autorelease];
	
	if ([category.status intValue] != STATUS_DELETED)
	{
		[allChildren addObject:category];
		[indentations setObject:[NSNumber numberWithInt:indent] forKey:[category objectID]];
		
		NSMutableArray *children = [NSMutableArray arrayWithArray:[[category children] allObjects]];
		[children sortUsingFunction:&compareCategories context:NULL];

		for (CDCategory *child in children)
		{
			[allChildren addObjectsFromArray:expandChildren(child, indentations, indent + 1)];
		}
	}
		
	return allChildren;
}

@implementation BaseCategoryViewController

#pragma mark View controller methods

- (void)viewDidLoad
{
	categories = [[NSMutableArray alloc] init];
	indentations = [[NSMutableDictionary alloc] init];

	if (UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPad)
	{
		self.tableView.separatorStyle = UITableViewCellSeparatorStyleNone;
	}

	[self loadCategories];

	[super viewDidLoad];
}

- (void)viewDidUnload
{
	[categories release];
	categories = nil;
	
	[indentations release];
	indentations = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)toInterfaceOrientation
{
	return YES;
}

#pragma mark Object lifetime

- (void)dealloc
{
	[self viewDidUnload];
	
	[super dealloc];
}

#pragma mark Domain methods

- (void)loadCategories
{
	[categories removeAllObjects];
	[indentations removeAllObjects];

	// We're assuming that there are not a bunch of categories, therefore we keep them in memory.
	// This is not the case with tasks.

	NSFetchRequest *request = [[NSFetchRequest alloc] init];
	[request setEntity:[NSEntityDescription entityForName:@"CDCategory" inManagedObjectContext:getManagedObjectContext()]];
	[request setPredicate:[NSPredicate predicateWithFormat:@"status != %d AND file == %@ AND parent == NULL", STATUS_DELETED,
						   [Configuration configuration].cdCurrentFile]];
	NSSortDescriptor *sd = [[NSSortDescriptor alloc] initWithKey:@"name" ascending:YES];
	[request setSortDescriptors:[NSArray arrayWithObject:sd]];
	[sd release];
	
	NSError *error;
	NSArray *rootItems = [getManagedObjectContext() executeFetchRequest:request error:&error];
	[request release];

	if (!rootItems)
	{
		JLERROR("Could not fetch categories: %s", [[error localizedDescription] UTF8String]);
		return;
	}

	for (CDCategory *category in rootItems)
	{
		JLDEBUG("Root category: \"%s\"", [category.name UTF8String]);

		[categories addObjectsFromArray:expandChildren(category, indentations, 0)];
	}
}


- (void)fillCell:(BadgedCell *)cell forCategory:(CDCategory *)category
{
	[cell.badge clearAnnotations];
	cell.badge.text = nil;

	cell.textLabel.text = category.name;
	cell.textLabel.textColor = [UIColor blackColor];

	cell.indentationLevel = [[indentations objectForKey:[category objectID]] intValue];
	cell.indentationWidth = 15;
	cell.accessoryType = UITableViewCellAccessoryNone;
}

#pragma mark Table view methods

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return [categories count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
	BadgedCell * cell = nil;

	static NSString *CellIdentifier = @"BadgedCell";

	if (UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPhone)
		cell = (BadgedCell *)[tableView dequeueReusableCellWithIdentifier:CellIdentifier];

	if (cell == nil)
	{
		cell = [[[CellFactory cellFactory] createBadgedCell] autorelease];
	}

	CDCategory *category = [categories objectAtIndex:indexPath.row];
	[self fillCell:cell forCategory:category];
	
    return cell;
}

@end

