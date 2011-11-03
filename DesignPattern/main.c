#include "stdio.h"
extern a;
int main(int argc, const char *argv[])
{
    a = 45;
    printf("%d\n", sizeof(a));
    
    return 0;
}
