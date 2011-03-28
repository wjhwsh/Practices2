#include <iostream>
using namespace std;
int add(int a, int b=0)
{
    return a+b;
}
int main(int argc, char ** argv)
{
    cout<<"\t\n"<<add(1)<<endl;
    return 0;
}
