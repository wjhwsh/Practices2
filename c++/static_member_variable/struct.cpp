#include <iostream>
#include "rsContext.h"


using namespace std;
using namespace android::renderscript;

struct Context::Props Context::props;
int main(int argc, const char *argv[])
{
    if (Context::props.mRemoteClient)
        cout << "True" << endl;
    cout << Context::props.mRemoteIP << endl;
    Context c;
    cout << Context::props.mRemoteIP << endl;
    Context::props.mRemoteIP = 127001;
    cout << Context::props.mRemoteIP << endl;
    return 0;
}

