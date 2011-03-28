#include <iostream>
#include <algorithm>
using namespace std;

void perm(int *list, int start, int n)
{
    static int count = 0;
    int j,temp;
    if (start == n) {
        cout << "[" << count << "]: \t";
        for(j = 0; j < n; j++)
            cout << list[j] << ", ";
        cout << "\n" ;
        count++;
    } else {
        for(j = start; j < n; j++) {
            swap(list[start], list[j]);
            perm(list, start+1,n);
            swap(list[start], list[j]);
        }
    }
}

int main(int argc, char **argv)
{
    int array[4] = { 1, 2, 3, 4 };
    
    perm(array, 2, 4);

    for(int j = 0; j < sizeof(array)/sizeof(int); j++)
        cout << array[j] << ", ";
    return 0;
}
