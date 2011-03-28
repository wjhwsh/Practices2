//
//  PicnicViewController.h
//  Picnic
//
//  Created by Ray Wenderlich on 12/8/10.
//  Copyright 2010 Ray Wenderlich. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface PicnicViewController : UIViewController {
    bool bugDead;
}

@property (assign) IBOutlet UIImageView *basketTop;
@property (assign) IBOutlet UIImageView *basketBottom;
@property (assign) IBOutlet UIImageView *napkinTop;
@property (assign) IBOutlet UIImageView *napkinBottom;
@property (assign) IBOutlet UIImageView *bug;

@end

