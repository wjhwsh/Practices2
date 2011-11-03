#include <iostream>
using namespace std;

class Board {
    Board(){value = 999;}
    ~Board() {};
    Board(const Board &b) { m_pInstance = } 
    static Board *m_pInstance;
    int value;

public:
    static Board *self() {
        if ( m_pInstance == 0)
            m_pInstance = new Board();
        return m_pInstance;
    }
    int get_value() { return value; }
    void set_value(int v) { value = v; }
};

Board *Board::m_pInstance = 0;

int main(int argc, const char *argv[])
{
    Board *bptr = new Board(*Board::self());
    cout << Board::self()->get_value() << endl;
    //delete Board::self();
    //cout << Board::p << endl;
    return 0;
}
