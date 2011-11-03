//
//  CheckView.h
//  TaskCoach
//
//  Created by Jérôme Laheurte on 17/01/09.
//  Copyright 2009 Jérôme Laheurte. See COPYING for details.
//

#import <Foundation/Foundation.h>

@interface CheckView : UIImageView
{
	id target;
	SEL action;
}

- (void)setTarget:(id)target action:(SEL)action;

@end
