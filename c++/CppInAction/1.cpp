#include <iostream>

using namespace std;

class World {

private:

    int init_num;

public:
    
    World() {
        init_num = 999;
        cout << "Initiating: " << init_num << endl;
    }
    
    void hello() { cout<<"Hello from 1! Good bye from 1. Hello from 2! Good bye from 2. number: " << init_num; }
    static void hello2() { cout<<"Hello from 1! Good bye from 1. Hello from 2! Good bye from 2."; }
};

class World2 {
    public:
        World2(int i) {
            cout << "Hello from "<< i << "! Good bye from " << i << endl;
        }
};

int main(int argc, char **argv) {

    World a = World();
    a.hello();
    cout << endl;
    World::hello2();
    
    cout << endl << "--------------------The correct answer--------------------" << endl;
    
    for( int i = 1; i < 3; i++) {
        World2 a(i);
    }

    {
        World2 a(1);
    }

    {
        World2 a(2);
    }



    return 0;
}
