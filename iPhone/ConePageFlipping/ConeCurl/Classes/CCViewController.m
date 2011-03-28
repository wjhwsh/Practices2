//
//  CCViewController.m
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/28/10.
//  Copyright 2010 W. Dana Nuon. All rights reserved.
//

#import "CCViewController.h"
#import "CCCommon.h"
#import "EAGLView.h"
#import "CCPage.h"


@interface CCViewController ()
// Empty category for "private" methods
- (void)updateSliders;
@end

@implementation CCViewController

@synthesize glView;
@synthesize animateSwitch;
@synthesize timeSlider, timeLabel;
@synthesize rhoSlider, rhoLabel;
@synthesize thetaSlider, thetaLabel;
@synthesize aSlider, aLabel;


/*
 // The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
    }
    return self;
}
*/


- (void)viewDidLoad
{
  [super viewDidLoad];
  [self updateSliders];
}


- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Overriden to allow any orientation.
    return YES;
}


- (void)didReceiveMemoryWarning {
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}


- (void)viewDidUnload {
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}


- (void)dealloc
{
	if (timer_ != nil)
  {
		[timer_ invalidate];
    timer_ = nil;
  }
  [animateSwitch release];
  [timeSlider release];
  [timeLabel release];
  [glView release];
  [super dealloc];
}

- (void)startAnimation
{
  [glView startAnimation];
	if (timer_ != nil)
  {
		[timer_ invalidate];
  }
	timer_ = [NSTimer scheduledTimerWithTimeInterval:1.0f / 30
                                            target:self 
                                          selector:@selector(updateSliders) 
                                          userInfo:nil
                                           repeats:YES];
  animateSwitch.on = YES;
}

- (void)stopAnimation
{
  [glView stopAnimation];
	if (timer_ != nil)
  {
		[timer_ invalidate];
    timer_ = nil;
  }
  animateSwitch.on = NO;
}

- (IBAction)switchValueChanged:(id)sender
{
  UISwitch *switch_;
  if ([sender isKindOfClass:[UISwitch class]])
    switch_ = (UISwitch *)sender;
  else
    return;
  
  if ([switch_ isEqual:animateSwitch])
  {
    if (switch_.on)
      [self startAnimation];
    else
      [self stopAnimation];
  }
}

- (IBAction)sliderValueChanged:(id)sender
{
  UISlider *slider;
  if ([sender isKindOfClass:[UISlider class]])
    slider = (UISlider *)sender;
  else
    return;
  
  UILabel *sliderLabel;
  CGFloat value = [slider value];
  CCPage *page = [glView activePage];
  if ([slider isEqual:timeSlider])
  {
    sliderLabel = timeLabel;
    value = 1.0f - value;
    [page deformForTime:(value)];
    glView.animationTime = value;
    [self updateSliders];
  }
  else if ([slider isEqual:rhoSlider])
  {
    sliderLabel = rhoLabel;
    value = 180.0f - value;
    page.rho = DEGREES_TO_RADIANS(value);
    [page deform];
  }
  else if ([slider isEqual:thetaSlider])
  {
    sliderLabel = thetaLabel;
    page.theta = DEGREES_TO_RADIANS(value);
    [page deform];
  }
  else if ([slider isEqual:aSlider])
  {
    sliderLabel = aLabel;
    page.A = value;
    [page deform];
  }
  else
    return;

  if (timer_ != nil)
    [self stopAnimation];
  [glView drawView:nil];
  NSString *valueString = [NSString stringWithFormat:@"%0.2f", value];
  sliderLabel.text = valueString;
}

#pragma mark -
#pragma mark Private methods

- (void)updateSliders
{
  CCPage *page      = [glView activePage];
  timeSlider.value  = 1.0f - glView.animationTime;
  rhoSlider.value   = 180.0f - page.rho * RAD;
  thetaSlider.value = page.theta * RAD;
  aSlider.value     = page.A;
  timeLabel.text    = [NSString stringWithFormat:@"%0.2f", timeSlider.value];
  rhoLabel.text     = [NSString stringWithFormat:@"%0.2f", rhoSlider.value];
  thetaLabel.text   = [NSString stringWithFormat:@"%0.2f", thetaSlider.value];
  aLabel.text       = [NSString stringWithFormat:@"%0.2f", aSlider.value];
}


@end
