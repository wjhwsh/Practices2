//
//  OpenGLBasicsAppDelegate.m
//  OpenGLBasics
//
//  Created by Charlie Key on 6/24/09.
//

#import "OpenGLBasicsAppDelegate.h"
#import "EAGLView.h"
#import "CView.h"
@interface CustomUIView : UIView
{
	
}

@end

@implementation CustomUIView
- (id)initWithFrame:(CGRect)frame {
    
    self = [super initWithFrame:frame];
    if (self) {
        self.backgroundColor = [UIColor whiteColor];
    }
    return self;
}
/*-(void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
	NSLog(@"hello, touches on CustomUIView");
}
-(void)touchesMoved:(NSSet *)touches withEvent:(UIEvent *)event {
	NSLog(@"moving in CustomUIView");
}*/

@end


@implementation OpenGLBasicsAppDelegate

@synthesize window;
@synthesize glView;

- (void)applicationDidFinishLaunching:(UIApplication *)application {
  
  //No need for nib
  window = [[UIWindow alloc] initWithFrame:[UIScreen mainScreen].bounds];
  glView = [[EAGLView alloc] initWithFrame:window.bounds];
  [window addSubview:glView];
	CustomUIView *view = [[CustomUIView alloc] initWithFrame:CGRectMake(0, 0, 320, 240)];
	[window addSubview:view];
	
  [window makeKeyAndVisible];
  
	glView.animationInterval = 1.0 / 60.0;
	[glView startAnimation];
}


- (void)applicationWillResignActive:(UIApplication *)application {
	glView.animationInterval = 1.0 / 5.0;
}


- (void)applicationDidBecomeActive:(UIApplication *)application {
	glView.animationInterval = 1.0 / 60.0;
}


- (void)dealloc {
	[window release];
	[glView release];
	[super dealloc];
}

@end
