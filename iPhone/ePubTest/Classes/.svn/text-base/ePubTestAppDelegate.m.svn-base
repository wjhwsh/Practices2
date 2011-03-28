//
//  ePubTestAppDelegate.m
//  ePubTest
//
//  Created by Bob Wei on 4/3/10.
//  Copyright Apple Inc 2010. All rights reserved.
//

#import "ePubTestAppDelegate.h"
#import "ePubTestViewController.h"

@implementation ePubTestAppDelegate

@synthesize window;
@synthesize viewController;


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {    
    
    // Override point for customization after app launch    
    [window addSubview:viewController.view];
    [window makeKeyAndVisible];
	
	[[UIApplication sharedApplication] setStatusBarHidden:YES];
	[[UIApplication sharedApplication] setStatusBarStyle:UIStatusBarStyleBlackTranslucent];
	
	return YES;
}


- (void)dealloc {
    [viewController release];
    [window release];
    [super dealloc];
}


@end
