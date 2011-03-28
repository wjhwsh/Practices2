#include <stdio.h>
#include <math.h>

void printBinary(int x) {
    int bits = sizeof(x) * 8;
    unsigned int mask = exp2(bits-1);

    int i;
    for(i = 0; i < bits; ++i, mask = mask >> 1) {

        printf("%d", (mask & x) ? 1 : 0);
    }
}

int main (int argc, char ** argv) 
{
    int a = 0;
    //printBinary(a);
    char *ptr = (char*)&a;
    int i;
    for (i = 0; i < sizeof(a); ++i, ++ptr) {
        printf("%d, address: %p\n", (int)*ptr, ptr);
    
    }

    return 0;
}
