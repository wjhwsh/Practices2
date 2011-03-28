//
//  CView.m
//  OpenGLBasics
//
//  Created by Kordan on 2011/1/6.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "CView.h"


@implementation CView


- (id)initWithFrame:(CGRect)frame {
    
    self = [super initWithFrame:frame];
    if (self) {
        self.backgroundColor = [UIColor whiteColor];
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect {
    // Drawing code.
}
*/

-(void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
	NSLog(@"hello, touches on CView");
}

- (void)dealloc {
    [super dealloc];
}


@end
