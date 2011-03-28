#include <iostream>
#include "Sema.h"
using namespace std;
using namespace sema;


class MySema : public Sema {
public:
    using Sema::func;
    void func() { cout << "I'm the customized function in MySema." << endl; }
    void test() {
        Sema::func();
        func();
        cout << "test() in MySema" << endl;
    }
};

class Driver {
    Sema &sema;
public:
    Driver(Sema &s) : sema(s){}
    void act() { 
        sema.func();
    }
}; 

int main(int arhc, char **argv) 
{
    MySema *mySema = new MySema();
    ((Sema*)mySema)->func();
    //mySema.func();
    //Driver d(mySema);
    //d.act();


    return 0;
}
