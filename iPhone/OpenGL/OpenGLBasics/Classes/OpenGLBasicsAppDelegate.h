//
//  OpenGLBasicsAppDelegate.h
//  OpenGLBasics
//
//  Created by Charlie Key on 6/24/09.
//

#import <UIKit/UIKit.h>

@class EAGLView;

@interface OpenGLBasicsAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    EAGLView *glView;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet EAGLView *glView;

@end

