//
//  TaskCoachAppDelegate.h
//  TaskCoach
//
//  Created by Jérôme Laheurte on 14/01/09.
//  Copyright Jérôme Laheurte 2009. See COPYING for details.
//

#import <UIKit/UIKit.h>

@class CategoryViewController;
@class CategoryTaskViewController;

@interface TaskCoachAppDelegate : NSObject <UIApplicationDelegate>
{
    NSManagedObjectModel *managedObjectModel;
    NSManagedObjectContext *managedObjectContext;	    
    NSPersistentStoreCoordinator *persistentStoreCoordinator;
	
    UIWindow *window;
	UIViewController *mainController;
}

@property (nonatomic, retain, readonly) NSManagedObjectModel *managedObjectModel;
@property (nonatomic, retain, readonly) NSManagedObjectContext *managedObjectContext;
@property (nonatomic, retain, readonly) NSPersistentStoreCoordinator *persistentStoreCoordinator;

@property (nonatomic, readonly) NSString *applicationDocumentsDirectory;

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet UIViewController *mainController;

@end

// Utility functions

NSManagedObjectContext *getManagedObjectContext(void);
