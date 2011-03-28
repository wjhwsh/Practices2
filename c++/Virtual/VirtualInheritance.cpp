#include <iostream>
using namespace std;

class A {
public:
    A() { cout << "A constructs." << endl; }
    void printStr() { cout << "Hello" << endl; }
};

class B1 : public A {
public:
    B1() { cout << "B1 constructs." << endl; }
};

class B2 : virtual public A {
public:
    B2() { cout << "B2 constructs." << endl; }
};

class C : public B1, B2 {
public:
    C() { cout << "C constructs." << endl; }
};


int main(int argc, char **argv)
{
    C c;
    c.printStr();
    return 0;
}
