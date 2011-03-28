#include <iostream>
using namespace std;

class Hand 
{
    private:
        int _n;
    public:
        Hand(int n) {
            _n = n;
        }

};

class Glove
{
public:
    Glove (int cFingers)
    : _n (cFingers), _hand (cFingers)
    {
        cout << "Glove with " << _n << " fingers\n";
    }
private:
    //Hand  _hand;
    //int   _n;
    // #1. the order of preamble initialization should be the same with the order of which they are embedded in Glove,
    //     so we reorder that.
    // #2. replace _n with cFingers, without changing the order.
    Hand _hand;
    int _n;
};

 
int main(int argc, char **argv) {
    return 0;
}
