#include <iostream>
using namespace std;

    int f(int a) {
        cout << "A: int f(int), " << a << endl;
        return a;
    }
    char f(char a) {
        cout << "A: char f(char), " << a << endl;
    }

    double f(double a) {
        cout << "B: double f(double), " << a << endl;
        return a;
    }
int main(int argc, char **argv) {

    f(1.0);
    f(2);
    f('3');

    return 0;
}
