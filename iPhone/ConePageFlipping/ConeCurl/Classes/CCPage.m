//
//  CCPage.m
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/18/10.
//  Copyright 2010 W. Dana Nuon. All rights reserved.
//


#import "CCPage.h"
#import "CCViewController.h"


@interface CCPage ()
// Empty category for "private" methods
- (void)createTriangleArray;
- (void)createTriangleStrip;
@end


@implementation CCPage

@synthesize width, height, columns, rows;
@synthesize currentFrame, framesPerCycle;
@synthesize rho, theta, A;


- (id)init
{
	if (self = [super init])
	{
    width         = 0.8f;
    height        = 1.0f;
    columns       = 8;
    rows          = 10;
    theta         = 90.0f;
    rho           = 0.0f;
    A             = 0.0f;
	}
	return self;
}

- (void)dealloc
{
  if (inputMesh_ != NULL)
    free(inputMesh_);
  if (outputMesh_ != NULL)
    free(outputMesh_);
  if (textureArray_ != NULL)
    free(textureArray_);
  if (triangles_ != NULL)
    free(triangles_);
  if (faces_ != NULL)
    free(faces_);
  if (frontStrip_ != NULL)
    free(frontStrip_);
  if (backStrip_ != NULL)
    free(backStrip_);
  
	[super dealloc];
}

- (const Vertex2f *)textureArray
{
  return textureArray_;
}

- (const Vertex3f *)vertices
{
  return outputMesh_;
}

- (const u_short *)frontFaces
{
  return faces_;
}

- (const u_short *)backFaces
{
  // Return an offset since we store both front and back triangle arrays together in one array.
  return faces_ + numFaces_ * 3;
}

- (u_short)numFaces
{
  return numFaces_;
}

- (const u_short *)frontStrip
{
  return frontStrip_;
}

- (const u_short *)backStrip
{
  return backStrip_;
}

- (u_short)stripLength
{
  return stripLength_;
}

- (void)createMesh
{
  u_short vCountX = columns + 1; // Number of vertices along the x axis
  u_short vCountY = rows + 1; // Number of vertices along the y axis
  numFaces_ = columns * rows * 2;
  
  numVertices_  = vCountX * vCountY;
  if (inputMesh_ != NULL)
    free(inputMesh_);
  inputMesh_ = malloc(sizeof(Vertex2f) * numVertices_);
  if (outputMesh_ != NULL)
    free(outputMesh_);
  outputMesh_ = malloc(sizeof(Vertex3f) * numVertices_);
  if (textureArray_ != NULL)
    free(textureArray_);
  textureArray_ = malloc(sizeof(Vertex2f) * numVertices_);
    
  u_short vi = 0;	// vertex index
  short iiX, iiY;
  CGFloat px, py;
  // Create our flat page geometry as a vertex array. Even though our page has two sides, we need to generate only one
  // set of vertices since the front and back are coplanar meshes.
  for (iiY = 0; iiY < vCountY; iiY++)
  {
    for (iiX = 0; iiX < vCountX; iiX++)
    {
      px = (CGFloat)iiX * width / columns;
      py = (CGFloat)iiY * height / rows;
      inputMesh_[vi].x = px;
      inputMesh_[vi].y = py;
      textureArray_[vi].x = (CGFloat)iiX / columns;
      textureArray_[vi].y = (CGFloat)(iiY) / rows;
      vi++;
//      NSLog(@"%d: (%d, %d) = (%0.2f, %0.2f)", vi, iiX, iiY, px, py);
    }
  }

  // Once we have our basic page geometry, tesselate it into an array of discrete triangles or triangle strips.
#if USE_TRIANGLE_STRIPS
  [self createTriangleStrip];
#else
  [self createTriangleArray];
#endif
  
}

- (void)incrementTime
{
  currentFrame++;
  currentFrame %= framesPerCycle;
}

- (CGFloat)currentTime
{
  return (CGFloat)currentFrame / framesPerCycle;
}

- (void)deformForTime:(CGFloat)t
{
  // This method computes rho, theta, and A for time parameter t using pre-defined functions to simulate a natural page turn
  // without finger tracking, i.e., for a quick swipe of the finger to turn to the next page.
  // These functions were constructed empirically by breaking down a page turn into phases and experimenting with trial and error
  // until we got acceptable results. This basic example consists of three distinct phases, but a more elegant solution yielding
  // smoother transitions can be obtained by curve fitting functions to our key data points once satisfied with the behavior.
	CGFloat angle1 =  90.0f / RAD;  //  }
  CGFloat angle2 =   8.0f / RAD;  //  }
  CGFloat angle3 =   6.0f / RAD;  //  }
  CGFloat     A1 = -15.0f;        //  }
  CGFloat     A2 =  -2.5f;        //  }--- Experiment with these parameters to adjust the page turn behavior to your liking.
  CGFloat     A3 =  -3.5f;        //  }
  CGFloat theta1 =   0.05f;       //  }
  CGFloat theta2 =   0.5f;        //  }
  CGFloat theta3 =  10.0f;        //  }
  CGFloat theta4 =   2.0f;        //  }
  
  CGFloat f1, f2, dt;

  // Here rho, the angle of the page rotation around the spine, is a linear function of time t. This is the simplest case and looks
  // Good Enough. A side effect is that due to the curling effect, the page appears to accelerate quickly at the beginning
  // of the turn, then slow down toward the end as the page uncurls and returns to its natural form, just like in real life.
  // A non-linear function may be slightly more realistic but is beyond the scope of this example.
  rho = t * M_PI;
  
	if (t <= 0.15f)
	{
    // Start off with a flat page with no deformation at the beginning of a page turn, then begin to curl the page gradually
    // as the hand lifts it off the surface of the book.
		dt = t / 0.15;
		f1 = sin(M_PI * pow(dt, theta1) / 2.0);
		f2 = sin(M_PI * pow(dt, theta2) / 2.0);
    theta = funcLinear(f1, angle1, angle2);
		A = funcLinear(f2, A1, A2);
	}
	else if (t <= 0.4)
	{
    // Produce the most pronounced curling near the middle of the turn. Here small values of theta and A
    // result in a short, fat cone that distinctly show the curl effect.
		dt = (t - 0.15) / 0.25;
		theta = funcLinear(dt, angle2, angle3);
		A = funcLinear(dt, A2, A3);
	}
	else if (t <= 1.0)
	{
    // Near the middle of the turn, the hand has released the page so it can return to its normal form.
    // Ease out the curl until it returns to a flat page at the completion of the turn. More advanced simulations
    // could apply a slight wobble to the page as it falls down like in real life.
		dt = (t - 0.4) / 0.6;
		f1 = sin(M_PI * pow(dt, theta3) / 2.0);
		f2 = sin(M_PI * pow(dt, theta4) / 2.0);
		theta = funcLinear(f1, angle3, angle1);
		A = funcLinear(f2, A3, A1);
	}
  [self deform];
}

- (void)deform
{
  // This method must be called after any values of rho, theta, or A have been changed in order to update the output geometry.

  // This is the guts of the conical page deformation algorithm, using just basic trigonometry.
  // Since each vertex is independent of any other, these calculations are very well suited for parallelization using
  // blocks (i.e., for GCD), vertex shaders (OpenGL ES 2.0), or other available features.
  
	Vertex2f  vi;   // Current input vertex, iterated over the flat page input mesh (basic vertex array).
  Vertex3f  v1;   // First stage of the deformation, with only theta and A applied. This results in a curl, but no rotation.
  Vertex3f *vo;   // Pointer to the finished vertex in the output mesh, after applying rho to v1 with a basic rotation transform.
  
  // Iterate over the input mesh to deform each vertex.
	CGFloat R, r, beta;
  for (u_short ii = 0; ii < numVertices_; ii++)
  {
    vi    = inputMesh_[ii];                           // Get the current input vertex from our input mesh.
    R     = sqrt(vi.x * vi.x + pow(vi.y - A, 2.0f));  // Radius of the circle circumscribed by vertex (vi.x, vi.y) around A on the x-y plane.
    r     = R * sin(theta);                       // From R, calculate the radius of the cone cross section intersected by our vertex in 3D space.
    beta  = asin(vi.x / R) / sin(theta);          // Angle SCT, the angle of the cone cross section subtended by the arc |ST|.
    
    v1.x  = r * sin(beta);
    v1.y  = R + A - r * (1.0f - cos(beta)) * sin(theta); // *** MAGIC!!! ***
    v1.z  = r * (1.0f - cos(beta)) * cos(theta);

    // Apply a basic rotation transform around the y axis to rotate the curled page. These two steps could be combined
    // through simple substitution, but are left separate to keep the math simple for debugging and illustrative purposes.
    vo    = &outputMesh_[ii];
    vo->x = (v1.x * cos(rho) - v1.z * sin(rho));
    vo->y =  v1.y;
    vo->z = (v1.x * sin(rho) + v1.z * cos(rho));
  }  
}

#pragma mark -
#pragma mark Private methods

- (void)createTriangleArray
{  
  u_short vCountX  = columns + 1; // Number of vertices along the x axis
  u_short numQuads = columns * rows;
  numFaces_ = numQuads * 2;
  if (faces_ != NULL)
    free(faces_);
  faces_ = malloc(sizeof(u_short) * numFaces_ * 6);  // Store both front and back triangle arrays in one array.
  
  u_short vi = 0;	// vertex index  
  u_short index;
  u_short rowNum, colNum;
  u_short ll, lr, ul, ur;
	for (index = 0; index < numQuads; index++)
	{	
		rowNum = index / columns;
		colNum = index % columns;
		ll = (rowNum) * vCountX + colNum;
		lr = ll + 1;
		ul = (rowNum + 1) * vCountX + colNum;
		ur = ul + 1;
    // Make two triangles out of each quad.
    // Wind the front of the page counter-clockwise so we can view it straight on.
    QuadToTrianglesWindCCWSet(&faces_[vi], ul, ur, ll, lr);
    // Wind the back of the page clockwise so it's visible only when it's been flipped.
    QuadToTrianglesWindCWSet(&faces_[vi + numFaces_ * 3], ul, ur, ll, lr);
		vi += 6;
	}
}

- (void)createTriangleStrip
{
  // Standard algorithm for tesselating a grid into an optimized triangle strip without resorting to a complex Hamiltonian algorithm.
  
  u_short vCountX = columns + 1; // Number of vertices along the x axis
  u_short vCountY = rows + 1;    // Number of vertices along the y axis
  
  stripLength_ = (vCountX * 2) * (vCountY - 1) + (vCountY - 2);
  if (frontStrip_ != NULL)
    free(frontStrip_);
  frontStrip_ = malloc(sizeof(u_short) * stripLength_);
  if (backStrip_ != NULL)
    free(backStrip_);
  backStrip_ = malloc(sizeof(u_short) * stripLength_);
  
  // Construct a triangle strip by scanning back and forth up our mesh, inserting degenerate triangles as necessary
  // to link adjacent rows.
  short iiX, iiY;
  u_short rowOffset, index = 0;
  BOOL lastRow, oddRow;
  for (iiY = 0; iiY < rows; iiY++)
  {
    // For the front, go right to left for odd rows, left to right for even rows. Weaving back and forth rather
    // than always restarting each row on the same side allows us the graphics hardware to reuse cached vertex
    // calculations, per Apple's best practices.
    // Build the back at the same time by scanning in reverse.
    rowOffset = iiY * vCountX;
    lastRow   = (iiY == rows);
    oddRow    = (iiY & 1);
    for (iiX = 0; iiX <= columns; iiX++) 
    {
      if (oddRow)
      {
        frontStrip_[index]  = rowOffset + columns - iiX + vCountX;
        backStrip_[index++] = rowOffset + iiX + vCountX;
        frontStrip_[index]  = rowOffset + columns - iiX;
        backStrip_[index++] = rowOffset + iiX;
      }
      else
      {
        frontStrip_[index]  = rowOffset + iiX + vCountX;
        backStrip_[index++] = rowOffset + columns - iiX + vCountX;
        frontStrip_[index]  = rowOffset + iiX;
        backStrip_[index++] = rowOffset + columns - iiX;
      }
    } 
    // Unless we're on the last row, insert a degenerate vertex to enable us to connect to the next row.
    if (!lastRow)
    {
      if (oddRow)
      {
        frontStrip_[index]  = rowOffset + vCountX;
        backStrip_[index]   = rowOffset + vCountX + columns;
      }
      else
      {
        frontStrip_[index]  = rowOffset + vCountX + columns;
        backStrip_[index]   = rowOffset + vCountX;
      }
      index++;
    }
  }
}

@end







