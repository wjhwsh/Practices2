#include <stdio.h>
#define NDEBUG 1
#if !NDEBUG
#define DEBUG(str, arg) printf(x, y)
#else
#define DEBUG(str, arg) ((void)0)
#endif

int main(int argc, char **argv)
{
    int x = 2;
    DEBUG("The Value: %d", x); 
    return 0;
}

