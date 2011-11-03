//
//  DatePickerViewController.h
//  TaskCoach
//
//  Created by Jérôme Laheurte on 19/01/09.
//  Copyright 2009 Jérôme Laheurte. See COPYING for details.
//

#import <UIKit/UIKit.h>

@interface DatePickerViewController : UIViewController
{
	UIDatePicker *picker;
	NSDate *date;
	
	id target;
	SEL action;
}

@property (nonatomic, retain) IBOutlet UIDatePicker *picker;

- (IBAction)onConfirm:(UIButton *)button;
- (IBAction)onCancel:(UIButton *)button;

- initWithDate:(NSDate *)date target:(id)target action:(SEL)action;

- (void)setDate:(NSDate *)date target:(id)target action:(SEL)action;

@end
