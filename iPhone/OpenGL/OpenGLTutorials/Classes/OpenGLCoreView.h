/*

File: OpenGLCoreView.h
Abstract: A UIView subclass that allows for the rendering of OpenGL ES content
by a delegate that implements the OpenGLCoreViewDelegate protocol.

Version: 1.0


*/

#import <UIKit/UIKit.h>
#import <OpenGLES/EAGL.h>
#import <OpenGLES/ES1/gl.h>
#import <OpenGLES/ES1/glext.h>

@protocol OpenGLCoreViewDelegate;

@interface OpenGLCoreView : UIView
{
    @private
    // The pixel dimensions of the backbuffer
    GLint backingWidth;
    GLint backingHeight;
    
    EAGLContext *context;
    
    // OpenGL names for the renderbuffer and framebuffers used to render to this view
    GLuint viewRenderbuffer, viewFramebuffer;
    
    // OpenGL name for the depth buffer that is attached to viewFramebuffer, if it exists (0 if it does not exist)
    GLuint depthRenderbuffer;
    
    // An animation timer that, when animation is started, will periodically call -drawView at the given rate.
    NSTimer *animationTimer;
    NSTimeInterval animationInterval;
    
    // Delegate to do our drawing, called by -drawView, which can be called manually or via the animation timer.
    id<OpenGLCoreViewDelegate> delegate;
    
    // Flag to denote that the -setupView method of a delegate has been called.
    // Resets to NO whenever the delegate changes.
    BOOL delegateSetup;
}

@property(nonatomic, assign) id<OpenGLCoreViewDelegate> delegate;

-(void)startAnimation;
-(void)stopAnimation;
-(void)drawView;

@property NSTimeInterval animationInterval;

@end

@protocol OpenGLCoreViewDelegate<NSObject>

@required

// Draw with OpenGL ES
-(void)drawView:(OpenGLCoreView*)view;

@optional

// Called whenever you need to do some initialization before rendering.
-(void)setupView:(OpenGLCoreView*)view;

@end