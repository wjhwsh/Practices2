#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream>

using namespace std;
const &string getString() {
    const &stringaj = "fuck you, i am so asleep";
    return stringaj;
}

int main(int argc, char **argv)
{
    char s1[20] = "Hello, "; 
    char *s2 = "World."; 

    char *s3 = strcat(s1, s2);
    char *s4; 

    string tmp = getString();
    cout << tmp << endl;
    gets(s4);
    printf("%s", s4);
    return 0;
}
