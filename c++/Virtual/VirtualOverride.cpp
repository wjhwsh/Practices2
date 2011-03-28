#include <iostream>
using namespace std;

class Sema {
public:
    virtual void func() { cout << "I'm the function in Sema." << endl; }
};

class MySema : public Sema {
public:
    virtual void func() { cout << "I'm the customized function in MySema." << endl; }
};

int main(int arhc, char **argv) 
{
    Sema sema;
    MySema mySema;
    sema.func();


    return 0;
}
