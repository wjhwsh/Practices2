//
//  ConeCurlAppDelegate.m
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/18/10.
//  Copyright W. Dana Nuon 2010. All rights reserved.
//

#import "ConeCurlAppDelegate.h"
#import "CCViewController.h"

@implementation ConeCurlAppDelegate

@synthesize window, viewController;

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions   
{
  [window addSubview:viewController.view];
  [window makeKeyAndVisible];

  return YES;
}

- (void)applicationWillResignActive:(UIApplication *)application
{
  [viewController stopAnimation];
}

- (void)applicationDidBecomeActive:(UIApplication *)application
{
  [viewController startAnimation];
}

- (void)applicationWillTerminate:(UIApplication *)application
{
  [viewController stopAnimation];
}

- (void)dealloc
{
  [viewController release];
  [window release];
  
  [super dealloc];
}

@end
