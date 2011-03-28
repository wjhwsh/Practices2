#include <iostream>
#include <string>

using namespace std;

class Parent {
public:
    Parent() {}
    virtual void print() = 0;

};
class Child2 : public Parent {
public: 
    string name;
    Child2() { name = "Hello World2!\n";}
    virtual void print() {
        cout << name << endl;
    }
    
};

class Child : public Parent {
public: 
    string name;
    Parent *a;
    Child() { name = "Hello World!\n";}
    virtual void print();
    
};

void Child::print() {
    a = new Child2();
    //(dynamic_cast<Child2 *>(a))->print();
    a->print();
    cout << "Child's print()" << endl;
}

static Parent* doNothing() {
    return new Child();
}

int main(int argc, char **argv) 
{
    Parent *a = doNothing();
    dynamic_cast<Child*>(a)->print();
    //cout << a->name << endl;

    return 0;
}
