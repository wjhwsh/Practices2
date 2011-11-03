#include <iostream>
#include "rsContext.h"
using namespace std;
using namespace android::renderscript;

Context::Context() {
    props.mLogTimes = false;
    props.mLogScripts = false;
    props.mLogObjects = false;
    props.mLogShaders = false;
    props.mLogShadersAttr = false;
    props.mLogShadersUniforms = false;
    props.mLogVisual = false;
    props.mRemoteClient = false;
    props.mRemoteServer = false;
    props.mRemoteIP = 127000;
}

void Context::printSomething() {
    cout << props.mRemoteIP << endl;
}
