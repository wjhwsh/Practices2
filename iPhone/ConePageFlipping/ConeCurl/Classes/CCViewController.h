//
//  CCViewController.h
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/28/10.
//  Copyright 2010 W. Dana Nuon. All rights reserved.
//


@class EAGLView;

@interface CCViewController : UIViewController
{
@private
  IBOutlet EAGLView   *glView;
  IBOutlet UISwitch   *animateSwitch;
  IBOutlet UISlider   *timeSlider;
  IBOutlet UISlider   *rhoSlider;
  IBOutlet UISlider   *thetaSlider;
  IBOutlet UISlider   *aSlider;
  IBOutlet UILabel    *timeLabel;
  IBOutlet UILabel    *rhoLabel;
  IBOutlet UILabel    *thetaLabel;
  IBOutlet UILabel    *aLabel;
  
  NSTimer *timer_;
}

@property (nonatomic, retain) IBOutlet EAGLView *glView;
@property (nonatomic, retain) IBOutlet UISwitch *animateSwitch;
@property (nonatomic, retain) IBOutlet UISlider *timeSlider;
@property (nonatomic, retain) IBOutlet UISlider *rhoSlider;
@property (nonatomic, retain) IBOutlet UISlider *thetaSlider;
@property (nonatomic, retain) IBOutlet UISlider *aSlider;
@property (nonatomic, retain) IBOutlet UILabel  *timeLabel;
@property (nonatomic, retain) IBOutlet UILabel  *rhoLabel;
@property (nonatomic, retain) IBOutlet UILabel  *thetaLabel;
@property (nonatomic, retain) IBOutlet UILabel  *aLabel;

- (void)startAnimation;
- (void)stopAnimation;
- (IBAction)switchValueChanged:(id)sender;
- (IBAction)sliderValueChanged:(id)sender;

@end
