#include <cstdlib>
#include <iostream>
#include <sstream>

using namespace std;

int check(string str) {
    int inter;
    istringstream Ddd(str);

    for(int i=0; i<str.length(); i++)
        if(str[i]>57 || str[i]<48)   return 0;
    Ddd>>inter;
    return inter;
}

int main(void)
{
    string lineIn, Bbb;
    int Ccc,one;

    while(getline(cin,lineIn)){
        cout << lineIn << endl;
        istringstream stream_lineIn(lineIn);
        Ccc=0;

        while(stream_lineIn){
            // auto-devide
            stream_lineIn>>Bbb;
            cout << "String Value: " << Bbb << endl;

            // the keypoint of this problem is that all non-integer string will be converted to zero!!
            one=check(Bbb);
            Ccc+=one;
        }
        cout << Ccc-one << endl;
    }

    return 0;
}

 

