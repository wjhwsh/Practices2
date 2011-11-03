#include <iostream>
#include "xx.h"


void foo();
//struct Something::S Something::s;
//int Something::value;
int main()
{
    //Something::s.a = 10;
    Something::value = 10;

    foo();
    //std::cout << Something::s.a;
    std::cout << Something::value;

    return 0;
}

