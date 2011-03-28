//
//  ES2Renderer.h
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/18/10.
//  Copyright W. Dana Nuon 2010. All rights reserved.
//
//  Modified from Xcode OpenGL ES template project. Currently unused but left as a stub for future implementation.
//
//  TODO: Implement this class.
//        Perform all the deformation and rotation calculations as a vertex shader.


#import "ESRenderer.h"
#import <OpenGLES/ES2/gl.h>
#import <OpenGLES/ES2/glext.h>

@interface ES2Renderer : NSObject <ESRenderer>
{
@private
    EAGLContext *context;

    // The pixel dimensions of the CAEAGLLayer
    GLint backingWidth;
    GLint backingHeight;

    // The OpenGL ES names for the framebuffer and renderbuffer used to render to this view
    GLuint defaultFramebuffer, colorRenderbuffer;

    GLuint program;
}

- (void)setupView:(CAEAGLLayer *)layer;
- (BOOL)resizeFromLayer:(CAEAGLLayer *)layer;
- (void)renderObject:(id)obj;

@end

