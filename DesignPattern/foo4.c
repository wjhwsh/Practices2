#include <stdio.h>
void f(void);
int x;

int main(int argc, char **argv) 
{
    x = 12345;
    f();
    printf("%d\n", x);
    return 0;
}


