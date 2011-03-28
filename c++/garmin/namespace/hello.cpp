#include <iostream>
#include <string>
#include "name.h"
using namespace std;
using namespace llvm;

namespace llvm { string a = "hello"; }
int xx = 0;
namespace llvm { string c = "String C"; }

int main(int argc, char **argv)
{
    string a = "hello";
    cout << a << b << endl;
    cout << c << endl;
    return 0;
}
