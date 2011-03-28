#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main()
{
    //string s("Somewhere down the road");
    string s;
    getline(cin, s);
    istringstream iss(s);

    //do
    //{
        string sub;
        iss >> sub;
        cout << "Substring: " << sub << endl;
        iss >> sub;
        cout << "Substring: " << sub << endl;
    //} while (iss);

    return 0;
}


