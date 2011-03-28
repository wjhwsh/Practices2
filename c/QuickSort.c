#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) 
{
    if (*(int *)a < *(int *)b)
        return -1;
    else if (*(int *)a == *(int *)b)
        return 0;
    else 
        return 1;
}

int main(int argc, const char *argv[])
{
    int a[10] = {9, 7, 6, 1, 5, 3, 4, 2, 8, 10};

    qsort(a, sizeof(a)/sizeof(int), sizeof(int), compare);

    int i;
    for (i = 0; i < sizeof(a)/sizeof(int); ++i) {
         printf("%d\t", a[i]);
    }
    return 0;
}
