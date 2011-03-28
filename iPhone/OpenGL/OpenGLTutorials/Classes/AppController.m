/*
File: AppController.m
Abstract: UIApplication's delegate class and the central controller of the application.

Version: 1.0
*/

#import "AppController.h"

// CONSTANTS
#define kRenderingFrequency         30.0 // Hz

// MACROS
#define DEGREES_TO_RADIANS(__ANGLE__) ((__ANGLE__) / 180.0 * M_PI)

#define OLD_DRAW 0

// CLASS IMPLEMENTATION
@implementation AppController

- (void)drawView:(OpenGLCoreView*)view;
{

#pragma mark Tutotial 2 Drawing a Triangle
#pragma mark -
#if defined(TUTORIAL5)
	const GLfloat triVertices[] = {
		0.0f,  1.0f,  0.0f,		// 0 - top of the triangle
		-1.0f, -1.0f, 1.0f,		// 1 - SouthWest corner B+-----+G
		1.0f, -1.0f, 1.0f,		// 2 - SouthEast corner  | \ / |
		                        //			                R
		1.0f, -1.0f, -1.0f,		// 3 - NorthEast corner  | / \ |
		-1.0f, -1.0f, -1.0f		// 4 - NorthWest corner G+-----+B
	};
#else if defined (TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4)
	// defining an array of vertexes instead of using glBegin() and glEnd()
	/*
	glBegin(GL_TRIANGLES); // Drawing Using Triangles
		glVertex3f( 0.0f, 1.0f, 0.0f); // Top
		glVertex3f(-1.0f,-1.0f, 0.0f); // Bottom Left
		glVertex3f( 1.0f,-1.0f, 0.0f); // Bottom Right
	glEnd();
	*/
	const GLfloat triVertices[] = {
		0.0f,  1.0f,  0.0f,
		-1.0f, -1.0f,  0.0f,
		1.0f, -1.0f,  0.0f
	};
#endif

#pragma mark Tutotial 3 add colors for triangle
#pragma mark -
#if defined(TUTORIAL5)
	const GLubyte triColors[] = { 
		255,   0,   0,  0,             // Red 
		0,   255,   0,  0,             // Green 
		0,     0, 255,  0,             // Blue 
		0,   255,   0,  0,             // Green 
		0,     0, 255,  0              // Blue 
	};
#else if defined(TUTORIAL3) || defined(TUTORIAL4)
	
	const GLubyte triColors[] = { 
		255,   0,   0,            // Red 
		0,   255,   0,            // Green 
		0,     0, 255             // Blue 
	};

#endif

#pragma mark Tutotial 5 3D models and rotate
#pragma mark -

#if defined(TUTORIAL5)
	// We need the number of faces we will be rendering, this is 16 
	const GLint triIndexCount = 16;
	
	// List our indexes. The first number is the number of indexes in our face 
	// Followed by the RGB faces. these correspond to the order of the tricolors array. 
	// Keep that in mind as you order your indexes. 
	
	GLushort triIndexes[] = {
		//  #, R, G, B
		3, 0, 1, 2,		// front face - top, sw, se
		3, 0, 3, 2,		// right face - top, ne, se
		3, 0, 3, 4,		// back face - top, ne, nw
		3, 0, 1, 4		// left face - top, sw, nw
	};
	
	// Tutorial 5
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); 

#else if defined(TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4)
	glClear(GL_COLOR_BUFFER_BIT);
#endif	


#if defined(TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4) ||  defined(TUTORIAL5)
	// Because our draw code gets called every time by the animation timer we need to clear the screen 
	//	before we draw.
	// When we last left off in setupView, we were on the model view, so we will reset our position 
	//	so that other rotations don't compound our view and cause weird things to happen.
	glLoadIdentity(); // Reset The Current Modelview Matrix
	
	// Next we will move ourselves so that the triangle doesn't show up in the center of the screen.
	glTranslatef(0.0f,2.0f,-6.0f); // Move up 2 Units And Into The Screen 6.0
#endif
	
#if defined(TUTORIAL4) ||  defined(TUTORIAL5)
#pragma mark Tutotial 4 for adding rotation
#pragma mark -
	glRotatef(rtri,0.0f,1.0f,0.0f); // Rotate The Triangle On The Y axis (tutorial 4)
#endif
	
#if defined(TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4) ||  defined(TUTORIAL5)
	/*
	Now we are going to create a vertex point that contains our triangle's vertexes and enable the Vertex
	Array in OpenGL. We do this by telling glVertexPointer that we are giving it values in groups of 3, that
	they are floats, and that we want it to begin at the beginning of the array, and then tell it what array to use.
	*/
	glVertexPointer(3, GL_FLOAT, 0, triVertices);
	glEnableClientState(GL_VERTEX_ARRAY);
#endif	
	
#if defined(TUTORIAL3) || defined(TUTORIAL4) || defined(TUTORIAL5)
/*
	glColorPointer(3, GL_UNSIGNED_BYTE, 0, triColors); // 3 will not work and should change to 4
*/
#pragma mark Tutotial 3 add colors for triangle
#pragma mark -
	glColorPointer(4, GL_UNSIGNED_BYTE, 0, triColors); 
    glEnableClientState(GL_COLOR_ARRAY); 
#endif
	
	

#pragma mark Tutotial 5 for 3D model and rotate
#pragma mark -
#if defined(TUTORIAL5)
	for(int i = 0; i < triIndexCount; i += triIndexes[i] + 1) 
	{ 
		glDrawElements(GL_TRIANGLES, triIndexes[i], GL_UNSIGNED_SHORT, 
					   &triIndexes[i+1]); 
	} 
    glDisableClientState(GL_VERTEX_ARRAY); 
    glDisableClientState(GL_COLOR_ARRAY);
	const GLfloat cubeVertices[] = {
		-1.0f, 1.0f, 1.0f,	// 0, Top Left Front Of The Cube		   4+-----+5
		1.0f, 1.0f, 1.0f,	// 1, Top Right Front Of The Cube		   /|    /|
		1.0f,-1.0f, 1.0f,	// 2, Bottom Right Front Of The Cube	  / |7  / |
		-1.0f,-1.0f, 1.0f,	// 3, Bottom Left Front Of The Cube		0+-----+1 +6
		-1.0f, 1.0f,-1.0f,	// 4, Top Left Back Of The Cube			 |     |  /
		1.0f, 1.0f,-1.0f,	// 5, Top Right Back Of The Cube		 |     | /
		1.0f,-1.0f,-1.0f,	// 6, Bottom Right Back Of The Cube		3+-----+2
		-1.0f,-1.0f,-1.0f	// 7, Bottom Left Back Of The Cube
	};
	// We need the number of faces we will be rendering, this is 6 faces, 5 values per face 
	int cubeIndexCount = 30; 
	const GLushort cubeIndexes[] = { 
		4, 0, 1, 4, 5, // Top 
		4, 3, 2, 7, 6, // Bottom 
		4, 0, 1, 3, 2, // Front 
		4, 4, 5, 7, 6, // Back 
		4, 0, 4, 3, 7, // Left 
		4, 1, 5, 2, 6  // Right 
	}; 
	const GLubyte cubeColors[] = { 
		3,   0, 255,   0, // Top - Green 
		3, 255, 125,   0, // Bottom - Orange 
		3, 255,   0,   0, // Front - Red 
		3, 255, 255,   0, // Back - Yellow 
		3,   0,   0, 255, // Left - Blue 
		3, 255,   0, 255  // Right - Violet 
	}; 

	glLoadIdentity(); // Reset The Current Modelview Matrix 
	glTranslatef(0.0f,-2.0f,-6.0f); // Move Down 2  Units And Into The Screen 6.0 
	glRotatef(rquad,1.0f,1.0f,1.0f); // Rotate The Cube On all 3 axises 
	glVertexPointer(3, GL_FLOAT, 0, cubeVertices); 
    glEnableClientState(GL_VERTEX_ARRAY); 
	for(int i = 0, j = 0; i < cubeIndexCount; i += cubeIndexes[i] + 1, j += 
		cubeColors[j] + 1) 
	{ 
		glColor4f(cubeColors[j+1], cubeColors[j+2], cubeColors[j+3], 0.0); 
		glDrawElements(GL_TRIANGLE_STRIP, cubeIndexes[i], GL_UNSIGNED_SHORT, 
					   &cubeIndexes[i+1]);
	} 
	glDisableClientState(GL_VERTEX_ARRAY); 
	glVertexPointer(3, GL_FLOAT, 0, cubeVertices); 
	glDisableClientState(GL_VERTEX_ARRAY);
#endif
	
#if defined(TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4) || defined(TUTORIAL5)
	/*
	 Lastly we will be drawing our array on the screen. We tell it that it is a triangle strip, that we want it to
	 start at array index 0, and that we want it to use 3 vertexes from the array. We provided it with 3 sets of
	 3 vertexes, so that's what it will draw.
	 */
/*
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 3); // 3 does not work, 4 is OK below
*/
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
#endif	
	
#pragma mark Tutotial 4 for adding rotation
#pragma mark -
#if defined (TUTORIAL4) || defined(TUTORIAL5)
	rtri+=1.0f; 
	if(rtri > 360.0f) 
	{ 
		rtri -= 360.0f; 
	}
#endif	

#pragma mark Tutotial 5 Drawing 3D models that rotate
#pragma mark -
#if defined(TUTORIAL5)
	rquad-=0.75f; 
	if(rquad < -360.0f) 
	{ 
		rquad += 360.0f; 
	} 
#endif
	
	
}

-(void)setupView:(OpenGLCoreView*)view
{
#pragma mark Tutotial 2 Drawing a Triangle
#pragma mark -
#if defined (TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4) || defined(TUTORIAL5)
	// constants and a float for the size of the frustum
	const GLfloat zNear = 0.1,
                  zFar = 1000.0,
                  fieldOfView = 60.0;
	GLfloat size;
#endif

#pragma mark Tutotial 4 for adding rotation
#pragma mark -
#if defined (TUTORIAL4) || defined(TUTORIAL5)
	rtri = 0.0f;
#endif

#pragma mark Tutotial 5 3D model and rotate
#pragma mark -
#if defined (TUTORIAL5)
	rquad = 0.0f; 	
#endif
	
#pragma mark Tutotial 5 3D model and rotate
#pragma mark -
#if defined(TUTORIAL5)
	glEnable(GL_DEPTH_TEST); // Enables Depth Testing Tutorial 5
#endif
	
#if defined(TUTORIAL2) || defined(TUTORIAL3) || defined(TUTORIAL4) || defined(TUTORIAL5)
	// Set the OpenGL projection matrix
	glMatrixMode(GL_PROJECTION);

	// calculate the size of the frustum, and call glFrustum to give it our values. 
	// This will give us a nice screen to work with.
	size = zNear * tanf(DEGREES_TO_RADIANS(fieldOfView) / 2.0);
	CGRect rect = view.bounds;
	// use gluPerspective
    /*
	[self gluPerspective:60.0f:((GLfloat)rect.size.width/ 
								(GLfloat)rect.size.height):0.1f:1000.0f];

    */	
	glFrustumf(-size, size, -size / (rect.size.width / rect.size.height), size /
	(rect.size.width / rect.size.height), zNear, zFar);
	// set our viewport. This tells OpenGL how much room we have to work with.
	glViewport(0, 0, rect.size.width, rect.size.height);
	
	// Now that we are done, we need to enter model mode and load our identity matrix. 
	// This resets the view to the origin.

	//Make the OpenGL modelview matrix the default
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	// Clears the view with black
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

#endif	
	
}

- (void)applicationDidFinishLaunching:(UIApplication*)application
{
    CGRect                    rect = [[UIScreen mainScreen] bounds];
    
    //Create a full-screen window
    window = [[UIWindow alloc] initWithFrame:rect];
    
    //Create the OpenGL ES view and add it to the window
    OpenGLCoreView *glView = [[OpenGLCoreView alloc] initWithFrame:rect];
    [window addSubview:glView];

    glView.delegate = self;
    glView.animationInterval = 1.0 / kRenderingFrequency;
    [glView startAnimation];

    [glView release];
    
    //Show the window
    [window makeKeyAndVisible];
    
}

- (void)dealloc
{
    [window release];
    [super dealloc];
}


#pragma mark add gluPerspective
- (void)gluPerspective:(double)fovy :(double)aspect :(double)zNear :(double)zFar 
{ 
	// Start in projection mode. 
	glMatrixMode(GL_PROJECTION); 
	glLoadIdentity(); 
	double xmin, xmax, ymin, ymax; 
	ymax = zNear * tan(fovy * M_PI / 360.0); 
	ymin = -ymax; 
	xmin = ymin * aspect; 
	xmax = ymax * aspect; 
	glFrustumf(xmin, xmax, ymin, ymax, zNear, zFar); 
} 

@end
