#include <iostream>
using namespace std;

class Board {
    static int a;
};
Board b;

int Board::a = 999;

int main(int argc, const char *argv[])
{
    cout << Board::a << endl;
    cout << a << endl;
    
    return 0;
}
