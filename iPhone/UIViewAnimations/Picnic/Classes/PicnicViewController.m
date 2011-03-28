//
//  PicnicViewController.m
//  Picnic
//
//  Created by Ray Wenderlich on 12/8/10.
//  Copyright 2010 Ray Wenderlich. All rights reserved.
//

#import "PicnicViewController.h"
#import <AudioToolbox/AudioToolbox.h>

@implementation PicnicViewController
@synthesize basketTop;
@synthesize basketBottom;
@synthesize napkinTop;
@synthesize napkinBottom;
@synthesize bug;

/*
// The designated initializer. Override to perform setup that is required before the view is loaded.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}
*/


// Implement loadView to create a view hierarchy programmatically, without using a nib.
/*- (void)loadView {
    
}*/

- (void)viewTapped:(UITapGestureRecognizer *)sender {
    NSLog(@"View tapped!");
}

/*
- (void)moveToRight {
    [UIView animateWithDuration:1.0 
                          delay:2.0 
                        options:0
                     animations:^{                              
                         bug.center = CGPointMake(230, 250);
                     } 
                     completion:^(BOOL finished) {  
                         [UIView animateWithDuration:1.0 
                                               delay:0 
                                             options:0
                                          animations:^{                      
                                              bug.transform = CGAffineTransformMakeRotation(0);                                                           
                                          } completion:^(BOOL finished) {
                                              [self moveToLeft];
                                          }];                         
                     }];
}

- (void)moveToLeft {
    [UIView animateWithDuration:1.0 
                          delay:2.0 
                        options:0
                     animations:^{                              
                         bug.center = CGPointMake(75, 200);
                     } 
                     completion:^(BOOL finished) {  
                         [UIView animateWithDuration:1.0 
                                               delay:0 
                                             options:0
                                          animations:^{                      
                                              bug.transform = CGAffineTransformMakeRotation(M_PI);                                                           
                                          } completion:^(BOOL finished) {
                                              [self moveToRight];
                                          }];                         
                     }];    
}
*/

- (void)moveToLeft:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context {
 
    if (bugDead) return;
    [UIView beginAnimations:nil context:nil];
    [UIView setAnimationDuration:1.0];
    [UIView setAnimationDelay:2.0];
    [UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
    [UIView setAnimationDelegate:self];
    [UIView setAnimationDidStopSelector:@selector(faceRight:finished:context:)];
    bug.center = CGPointMake(75, 200);
    [UIView commitAnimations];
    
}

- (void)faceRight:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context {
    
    if (bugDead) return;
    [UIView beginAnimations:nil context:nil];
    [UIView setAnimationDuration:1.0];
    [UIView setAnimationDelay:0.0];
    [UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
    [UIView setAnimationDelegate:self];
    [UIView setAnimationDidStopSelector:@selector(moveToRight:finished:context:)];
    bug.transform = CGAffineTransformMakeRotation(M_PI);
    [UIView commitAnimations];
    
}

- (void)moveToRight:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context {
    
    if (bugDead) return;
    [UIView beginAnimations:nil context:nil];
    [UIView setAnimationDuration:1.0];
    [UIView setAnimationDelay:2.0];
    [UIView setAnimationDelegate:self];
    [UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
    [UIView setAnimationDidStopSelector:@selector(faceLeft:finished:context:)];
    bug.center = CGPointMake(230, 250);
    [UIView commitAnimations];
    
}

- (void)faceLeft:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context {
    
    if (bugDead) return;    
    [UIView beginAnimations:nil context:nil];
    [UIView setAnimationDuration:1.0];
    [UIView setAnimationDelay:0.0];
    [UIView setAnimationDelegate:self];
    [UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
    [UIView setAnimationDidStopSelector:@selector(moveToLeft:finished:context:)];
    bug.transform = CGAffineTransformMakeRotation(0);
    [UIView commitAnimations];
    
}

- (void) touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = [touches anyObject];
    CGPoint touchLocation = [touch locationInView:self.view];
    
    //CGRect bugRect = [bug frame];
    CGRect bugRect = [[[bug layer] presentationLayer] frame];
    if (CGRectContainsPoint(bugRect, touchLocation)) {
        NSLog(@"Bug tapped!");
    } else {
        NSLog(@"Bug not tapped.");
        return;
    }
    
    NSString *squishPath = [[NSBundle mainBundle] 
                            pathForResource:@"squish" ofType:@"caf"];
    NSURL *squishURL = [NSURL fileURLWithPath:squishPath];
    SystemSoundID squishSoundID;
    AudioServicesCreateSystemSoundID((CFURLRef)squishURL, &squishSoundID);
    AudioServicesPlaySystemSound(squishSoundID);
   
    bugDead = true;
    [UIView animateWithDuration:0.7 
                          delay:0.0 
                        options:UIViewAnimationCurveEaseOut
                     animations:^{                              
                         bug.transform = CGAffineTransformMakeScale(1.25, 0.75);
                     } 
                     completion:^(BOOL finished) {  
                         [UIView animateWithDuration:2.0 
                                               delay:2.0 
                                             options:0
                                          animations:^{                      
                                              bug.alpha = 0.0;
                                          } completion:^(BOOL finished) {
                                              [bug removeFromSuperview];
                                              bug = nil;
                                          }];                 
                     }];

}

// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
    
    //UITapGestureRecognizer *tapRecognizer = [[[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(viewTapped:)] autorelease];
    //[bug addGestureRecognizer:tapRecognizer];
    
    CGRect basketTopFrame = basketTop.frame;
    basketTopFrame.origin.y = -basketTopFrame.size.height;

    CGRect basketBottomFrame = basketBottom.frame;
    basketBottomFrame.origin.y = self.view.bounds.size.height;
     
    /* 
    //Pre iOS 4
    [UIView beginAnimations:nil context:nil];
    [UIView setAnimationDuration:0.5];
    [UIView setAnimationDelay:1.0];
    [UIView setAnimationCurve:UIViewAnimationCurveEaseOut];

    basketTop.frame = basketTopFrame;
    basketBottom.frame = basketBottomFrame;

    [UIView commitAnimations]; 
    */
    
    // iOS4+
    [UIView animateWithDuration:0.5
        delay:1.0
        options: UIViewAnimationCurveEaseOut
        animations:^{
            basketTop.frame = basketTopFrame;
            basketBottom.frame = basketBottomFrame;
        } 
        completion:^(BOOL finished){
            NSLog(@"Done!");
        }];
    
    CGRect napkinTopFrame = napkinTop.frame;
    napkinTopFrame.origin.y = -napkinTopFrame.size.height;    
    CGRect napkinBottomFrame = napkinBottom.frame;
    napkinBottomFrame.origin.y = self.view.bounds.size.height;

    [UIView animateWithDuration:0.7
                          delay:1.2
                        options: UIViewAnimationCurveEaseOut
                     animations:^{
                         napkinTop.frame = napkinTopFrame;
                         napkinBottom.frame = napkinBottomFrame;
                     } 
                     completion:^(BOOL finished){
                         NSLog(@"Done!");
                     }];
    
    
    [self moveToLeft:nil finished:nil context:nil];
        
}

/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
	
	// Release any cached data, images, etc that aren't in use.
}

- (void)viewDidUnload {
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}


- (void)dealloc {
    [super dealloc];
}

@end
