#include <iostream>

using namespace std;

class HorBar {
public:
    HorBar(int w) {
        cout << "+";
        for(int i = 0; i < w; i++)
            cout << "-";
        cout << "+" << endl;       
    }
};

class VerBar {
public:
    VerBar(int h) {
        for(int i = 0; i < h; i++)
            cout << "|" << endl;
    }
};

class Frame {
 public:
     Frame(int w, int h) 
     :_upper(w), _ver(h), _lower(w)
     { }
 private:
     HorBar _upper;
     VerBar _ver;
     HorBar _lower;
};

int main( int argc, char **argv) {

    Frame myFrame (10, 2);
    return 0;
}
