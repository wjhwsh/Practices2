//
//  Configuration.m
//  Task Coach
//
//  Created by Jérôme Laheurte on 13/03/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "Configuration.h"
#import "Task_CoachAppDelegate.h"

static Configuration *_instance = NULL;

static NSString *kCurrentListConfigName = @"currentList";
static NSString *kSoonDaysConfigName = @"soonDays";
static NSString *kGroupingConfigName = @"grouping";
static NSString *kRevertGroupingConfigName = @"revertGrouping";

/*
static NSString *kSectionsConfigName = @"sections";

@implementation TaskStatusSection

@synthesize condition, displayed;

- (id)initWithCondition:(NSString *)cond
{
    if ((self = [super init]))
    {
        condition = [cond copy];
        displayed = YES;
    }

    return self;
}

@end
*/

@implementation Configuration

@synthesize soonDays, grouping, revertGrouping;
// @synthesize sections;

- (id)init
{
    if ((self = [super init]))
    {
		NSUserDefaults *config = [NSUserDefaults standardUserDefaults];

        currentListURL = [[config URLForKey:kCurrentListConfigName] copy];

        soonDays = [config integerForKey:kSoonDaysConfigName];
        if (!soonDays)
            soonDays = 1;

        grouping = [config integerForKey:kGroupingConfigName];
        revertGrouping = [config boolForKey:kRevertGroupingConfigName];

        /*
        if ([config objectForKey:kSectionsConfigName])
        {
            // XXXTODO
        }
        else
        {
            // XXXTODO
        }
         */
    }

    return self;
}

+ (Configuration *)instance
{
    if (!_instance)
        _instance = [[Configuration alloc] init];
    return _instance;
}

- (void)save
{
    NSUserDefaults *config = [NSUserDefaults standardUserDefaults];
    [config setURL:currentListURL forKey:kCurrentListConfigName];
    [config setInteger:soonDays forKey:kSoonDaysConfigName];
    [config setInteger:grouping forKey:kGroupingConfigName];
    [config setBool:revertGrouping forKey:kRevertGroupingConfigName];

    [config synchronize];
}

#pragma mark - Properties

- (CDList *)currentList
{
    if (!currentListURL)
        return nil;

    NSManagedObjectID *objid = [getPersistentStoreCoordinator() managedObjectIDForURIRepresentation:currentListURL];
    CDList *list = (CDList *)[getManagedObjectContext() objectWithID:objid];

    return list;
}

- (void)setCurrentList:(CDList *)currentList
{
    [currentListURL release];
    currentListURL = [[[currentList objectID] URIRepresentation] copy];
}

- (NSString *)groupingName
{
    switch (self.grouping)
    {
        case GROUPING_PRIORITY:
            return @"priority";
        case GROUPING_START:
            return @"startDate";
        case GROUPING_DUE:
            return @"dueDate";
        default:
            return @"dateStatus";
    }
}

@end
