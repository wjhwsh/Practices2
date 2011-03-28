#include <iostream>
#include <string>
#include <fstream>
using namespace std;

int main(int argc, char ** argv) 
{
    ifstream inFile;
    inFile.open("/home/modcarl/workspace/HadoopPIPE/sample.txt");
    if (!inFile)
        cout << "not fount" << endl;

    string str;
    while (getline(inFile, str)) {
        cout << str.substr(0, 4) << endl;
        cout << str.substr(5, 7) << endl;
    }
    
    return 0;
}
