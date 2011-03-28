#include <iostream>
using namespace std;
class A {
public:
    int f(int a) {
        cout << "A: int f(int), " << a << endl;
        return a;
    }
    char f(char a) {
        cout << "A: char f(char), " << a << endl;
    }
};

class B {
public:
    double f(double a) {
        cout << "B: double f(double), " << a << endl;
        return a;
    }
};

class AB: public A, public B {
public:
    //using A::f; 
    // int A::f(int)
    // char A::f(char)
    //using B::f;
    // double B::f(double)

    char f(char a) {
        cout << "AB: char f(char), " << a << endl;
        return a;
    }
    //AB f(AB ab) {
    //    cout << "AB: AB f(AB), " << endl;
    //    return ab;
    //}
};

void g(AB &ab) {
    //ab.f(1);
    ab.f('a');
    //ab.f(2.0);
    //ab.f(ab);
}

int main(int argc, char **argv) {
    AB ab;
    g(ab);
    return 0;
}
