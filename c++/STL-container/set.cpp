#include <iostream>
#include <string>
#include <set>
#include <iterator>

using namespace std;

int main(int argc, char **argv) 
{
    set<string>::iterator si;

    set<string> strset1;
    strset1.insert("a");
    strset1.insert("a");
    strset1.insert("a");
    strset1.insert("b");
    strset1.insert("b");
    strset1.insert("c");

    set<string> strset2;
    strset2.insert("a");
    strset2.insert("a");
    strset2.insert("a");
    strset2.insert("b");
    strset2.insert("b");
    strset2.insert("c");

    // print strset1
    for (si = strset1.begin(); si != strset1.end(); ++si) {
        cout << *si << endl; 
    }

    copy(strset1.begin(), strset1.end(), ostream_iterator<string>(cout, " "));


    return 0;
}
