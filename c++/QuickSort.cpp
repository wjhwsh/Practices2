#include <iostream>
#include <algorithm>
using namespace std;

int swap(const void *elem1, const void *elem2) 
{
    int a = *(int*)elem1;
    int b = *(int*)elem2;
    
    if (a < b)
        return -1;
    else if (a > b)
        return 1;
    else
        return 0;
}
int main(int argc, char **argv) 
{
    int num[10] = {3, 5, 4, 1, 2, 7, 9, 10, 8, 6};
    qsort(num, 10, sizeof(int), swap);
    
    for (int i = 0; i < 10; i++)
        printf("%d\t", num[i]);
    printf("\n");

    return 0;
}
