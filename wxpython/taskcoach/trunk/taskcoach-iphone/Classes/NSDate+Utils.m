//
//  NSDate+Utils.m
//  TaskCoach
//
//  Created by Jérôme Laheurte on 09/05/10.
//  Copyright 2010 Jérôme Laheurte. All rights reserved.
//

#import "NSDate+Utils.h"


@implementation NSDate (Utils)

+ (NSDate *)dateRounded
{
	return [NSDate dateWithTimeIntervalSinceReferenceDate:60 * floor([[NSDate date] timeIntervalSinceReferenceDate] / 60)];
}

@end
