#include <stdio.h>
#include <math.h>

int main(int argc, char **argv)
{
    float eps = 0.000001;
    float x = 4; // circumference of the circumscribed (outside) regular polygon
    float y = 2 * sqrt(2); // circumference of the inscribed (inside) regular polygon
    float ctr = 0;
    float xnew = 0;

    while(x - y > eps) {
        // 2xy/(x+y) < x,  (2x^2/2x=x)=>(replace x with y)
        xnew = 2 * x * y / (x + y);
        // geometric mean
        y    = sqrt(xnew * y);
        x    = xnew;
        ctr += 1;
    }

    // 
    printf("PI = %f", (x+y)/2);
    printf("# of iterations = %f", ctr);
    return 0;
}
