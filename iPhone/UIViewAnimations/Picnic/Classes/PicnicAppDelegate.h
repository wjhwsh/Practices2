//
//  PicnicAppDelegate.h
//  Picnic
//
//  Created by Ray Wenderlich on 12/8/10.
//  Copyright 2010 Ray Wenderlich. All rights reserved.
//

#import <UIKit/UIKit.h>

@class PicnicViewController;

@interface PicnicAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    PicnicViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet PicnicViewController *viewController;

@end

