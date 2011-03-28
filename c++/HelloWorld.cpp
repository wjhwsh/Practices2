#include <iostream>

using namespace std;

void incByReference (int &a, int &b)
{
    (a++, b++);
}

void incByPointer (int *c, int *d)
{
    ((*c++), (++*d));
}


int main(void)
{
    string a = "1";
    int b = atoi(a);
    cout << b << endl;
    return 0;
}
