#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main( int argc, char **argv) {
    string s;
    int a, b;
    while(getline(cin, s)) {
        istringstream iss(s);

            iss >> a;
            iss >> b;
        cout <<a+b;
    }

    return 0;
}
