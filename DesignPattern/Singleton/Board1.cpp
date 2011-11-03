#include <iostream>
using namespace std;

class Board {
    Board(){value = 999;}
    ~Board() {}
    Board(const Board &b) {} 
    Board &operator=(const Board &b) {} 
    int value;

public:
    static Board *self() {
        static Board Instance;
        return &Instance;
    }
    int get_value() { return value; }
    void set_value(int v) { value = v; }
};


int main(int argc, const char *argv[])
{
    cout << Board::self()->get_value() << endl;
    //delete Board::self();
    //cout << Board::p << endl;
    return 0;
}
