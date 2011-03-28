//
//  ePubTestAppDelegate.h
//  ePubTest
//
//  Created by Bob Wei on 4/3/10.
//  Copyright Apple Inc 2010. All rights reserved.
//

#import <UIKit/UIKit.h>

@class ePubTestViewController;

@interface ePubTestAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    ePubTestViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet ePubTestViewController *viewController;

@end

