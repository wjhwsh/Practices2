#include <stdio.h>

__attribute__ ((weakref)) void foo();

int main(int arg, char **argv)
{   
    if(foo)foo();
    return 0;

}
