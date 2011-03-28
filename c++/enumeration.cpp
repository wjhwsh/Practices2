#include <iostream>
using namespace std;

enum {MON=1, TUE, WED, THU, FRI, STA, SUN};

typedef struct {
    short phone_num;
    int date;
    string name;
    double double_a;
    float float_b;
} Mystruct;

typedef union {
    int phone_num;
    int date;
    double double_a;
    float float_b;
} Myunion;

int main(int argc, char **argv) 
{
    switch(atoi(argv[1])) {
        case MON:
            cout << "Today is Monday" << endl;
            break;
        case TUE:
            cout << "Today is Tuesday" << endl;
            break;
        default:
            cout << "None of all" << endl;
            break;
    }

    Mystruct mystruct;
    mystruct.name = "Yao-Wei Ou";
    mystruct.date = 1;
    mystruct.phone_num = 123456;
    mystruct.double_a = 1.1;
    mystruct.float_b = 2.2;
    cout << "The size of mystruct is " << sizeof(mystruct) << endl;
    cout << "mystruct.name: " << mystruct.name << " size: " << sizeof(mystruct.name) << endl;
    cout << "mystruct.date: " << mystruct.date << " size: " << sizeof(mystruct.date) << endl;
    cout << "mystruct.phone_num: " << mystruct.phone_num << " size: " << sizeof(mystruct.phone_num) << endl;
    cout << "mystruct.double_a: " << mystruct.double_a << " size: " << sizeof(mystruct.double_a) << endl;
    cout << "mystruct.float_b: " << mystruct.float_b << " size: " << sizeof(mystruct.float_b) << endl;

    Myunion myunion;
    myunion.date = 1;
    myunion.phone_num = 123456;
    myunion.double_a = 1.1;
    myunion.float_b = 2.2;
    cout << "The size of myunion is " << sizeof(myunion) << endl;
    cout << "myunion.date: " << myunion.date << " size: " << sizeof(myunion.date) << endl;
    cout << "myunion.phone_num: " << myunion.phone_num << " size: " << sizeof(myunion.phone_num) << endl;
    cout << "myunion.double_a: " << myunion.double_a << " size: " << sizeof(myunion.double_a) << endl;
    cout << "myunion.float_b: " << mystruct.float_b << " size: " << sizeof(mystruct.float_b) << endl;
    return 0;
}
