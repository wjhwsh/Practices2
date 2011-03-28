#include <iostream>
using namespace std;

typedef void (*Callback_t)(string s);

static void printString(string s) {
    cout << s << endl;
}

class RSC {
public:
    RSC(){}

    Callback_t mLaunchCallback;
};

RSC *rsc = new RSC();

void after_running() {
    printf("printf: %p, &printf: %p", printf, &printf);
    void (*fp)(string s) = printString;
    Callback_t callback = fp; 
    rsc->mLaunchCallback = callback;
}


int main(int argc, char **argv)
{
    after_running();
    rsc->mLaunchCallback("Hello World");

    return 0;
}
