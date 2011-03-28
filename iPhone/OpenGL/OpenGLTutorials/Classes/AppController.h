/*

File: AppController.h
Abstract: UIApplication's delegate class and the central controller of the application.

Version: 1.0

*/

/*
TUTORIAL 1 : Setting up an OpenGL Project
TUTORIAL 2 : Drawing a Triangle
TUTORIAL 3 : Coloring the Triangle
TUTORIAL 4 : Rotating the Triangle
TUTORIAL 5 : Drawing 3D models that rotate
*/


#undef TUTORIAL5
#undef TUTORIAL4
#undef TUTORIAL3
#undef TUTORIAL2
#undef TUTORIAL1

// change this define to show other tutorials
#define TUTORIAL5




#import "OpenGLCoreView.h"

//CLASS INTERFACES:
@interface AppController : NSObject <OpenGLCoreViewDelegate>
{
    UIWindow*                window;

#if defined (TUTORIAL5) || defined(TUTORIAL4)
	// Tutorial 4 adding rotation to the triangle
	GLfloat rtri; // This will hold our value for how much we are rotating the triangle
#endif
#if defined (TUTORIAL5)
	// Tutorial 5 adding rotation to the 3D Model
	GLfloat rquad; // This will hold our value for how much we are rotating the 3D Model 
#endif
}

@end
