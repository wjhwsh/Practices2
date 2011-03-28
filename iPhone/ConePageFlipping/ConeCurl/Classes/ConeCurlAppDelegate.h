//
//  ConeCurlAppDelegate.h
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/18/10. @wdnuon
//  Copyright W. Dana Nuon 2010. All rights reserved.
//
//  Learn more at http://wdnuon.blogspot.com/2010/05/implementing-ibooks-page-curling-using.html
//

#import <UIKit/UIKit.h>

@class EAGLView, CCViewController;

@interface ConeCurlAppDelegate : NSObject <UIApplicationDelegate>
{
  IBOutlet UIWindow         *window;
  IBOutlet CCViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet CCViewController *viewController;

@end

