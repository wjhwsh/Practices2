#include <iostream> 
using namespace std; 

class Abstract {
public:
    Abstract() {}
    virtual void pure_virtual() = 0;
};

void Abstract::pure_virtual() {
    cout << "hello" << endl;
  // do something
}

class Child : public Abstract {
public:
   virtual void pure_virtual(); // no longer abstract, this class may be
                               // instantiated.
};

void Child::pure_virtual() {
  Abstract::pure_virtual(); // the implementation in the abstract class 
                            // is executed
}

int main() { 
    Abstract *a = new Child();
    a->pure_virtual();
    return 0;
}
