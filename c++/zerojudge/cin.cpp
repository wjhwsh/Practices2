#include <iostream>
#include <string>
using namespace std;

int main( int argc, char **argv) {
    string s;
  while(getline(cin, s))
       cout << "[" << s << "]" << endl;
    return 0;
}
