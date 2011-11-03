#include <iostream>
#include "main.h"
using namespace std;

void foo();

int Test::value;
int main(int argc, const char *argv[])
{
    Test t;
    t.value = 10;
    //t.doSomething(10);
    //foo();
    cout << Test::value << endl;
    
    return 0;
}
