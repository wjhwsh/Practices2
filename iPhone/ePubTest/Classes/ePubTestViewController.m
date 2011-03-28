//
//  ePubTestViewController.m
//  ePubTest
//
//  Created by Bob Wei on 4/3/10.
//  Copyright Apple Inc 2010. All rights reserved.
//

#import "ePubTestViewController.h"

@implementation ePubTestViewController



/*
// The designated initializer. Override to perform setup that is required before the view is loaded.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
    }
    return self;
}
*/

/*
// Implement loadView to create a view hierarchy programmatically, without using a nib.
- (void)loadView {
}
*/



// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
	[webView loadRequest:[NSURLRequest requestWithURL:[NSURL URLWithString:@"http://dl.dropbox.com/u/2531646/eBookRenderApp/columns.html"]]];
	webView.delegate = self;
}

-(void)webViewDidFinishLoad:(UIWebView *)awebView{
	NSLog(@"webViewDidFinishedLoad");
}

-(IBAction)next:(id)sender{
	[webView stringByEvaluatingJavaScriptFromString:@"nextPage();"];
	NSLog(@"currentPage = %@", [webView stringByEvaluatingJavaScriptFromString:@"getCurrentPage();"]);
}

-(IBAction)previous:(id)sender{
	[webView stringByEvaluatingJavaScriptFromString:@"previousPage();"];
	NSLog(@"currentPage = %@", [webView stringByEvaluatingJavaScriptFromString:@"getCurrentPage();"]);
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
