#include <iostream>
#include <string>
using namespace std; 

void gettok(string s)
{
    int CurC = s[0];
    int newToken = 1;
    int i = 1;
    int value = 0;
    string value_str = "";

    while(CurC != 0) {

        if(isdigit(CurC) && newToken) {
            newToken = 1;

            value_str += CurC;
        }

        if(isspace(CurC) || CurC == 0) {
            newToken = 1;

            value += atoi(value_str.c_str());    
            value_str = "";
        }
        
        if(!(isdigit(CurC) || isspace(CurC) || CurC == 0)) {
            newToken = 0;
            value_str = "";
        }

        CurC = s[i];
        i++;

    }

    value += atoi(value_str.c_str());

    cout << value << endl;


}

int main(int argc, char **argv) 
{
    string s;

    while(getline(cin, s)) 
        gettok(s);


    return 0;
}
