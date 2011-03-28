#include <iostream>
#include <string>

using namespace std;
int v = 0;
int _v = v;
int *p = &v;
int *_p = p;
string input;

int x = 1;
int *q = &x;

string command_list[] = {"reset", "x", "p++", "(*p)+1", "*p", "*p++", "v", "a", "exit"};

void execute (string input)
{          
    if(input == "reset") {
            v = _v;
            p = _p;
    } else if (input == "x") {   //arbitrary
            ;
            cout << "P The pointed value: " << (*p++ = *q++) << "\t\taddress: " << p << endl;
            cout << "Q The pointed value: " << *q << "\t\taddress: " << q << endl;
    } else if (input == "p++") {
            p++;
    } else if (input == "(*p)+1") {
            (*p)+1;
    } else if (input == "*p") {
            *p;
    } else if (input == "*p++") {
            *p++;
    } else if (input == "v") {
        cout << "\t\t\t" << *p << endl;
    } else if (input == "a") {
        cout << "\t\t\t" <<  p << endl;
    } else if (input == "exit") {
        ;
    } else {
            cout << "No such command. Please enter one of the following command list." << endl;
            int length = sizeof(command_list) / sizeof(command_list[0]); 
            cout << "--------------" << endl;
            for( int i = 0; i < length; i++)
                cout << command_list[i] << endl;
            cout << "--------------" << endl;
    }            
    cout << endl;

}

int main (int argc, char **argv)
{
    cout << "What is this expression "<< "*p++" <<" equivalent to?" << endl;
    execute("*p++");
    cout << "\n*p++" << endl;
    cout << "The pointed value: " << *p << "\t\taddress: " << p << endl;
    execute("reset");
    while(input != "exit") {
        getline(cin, input);
        execute(input);
    } 

    return 0;
}
