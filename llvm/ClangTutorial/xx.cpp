#include <iostream>
//#include "clang/Frontend/FrontendAction.h"
//#include "clang/Frontend/CompilerInvocation.h"
//#include "clang/Basic/LangOptions.h"
#include "header.h"
using namespace std;


int main(int argc, char **argv) 
{
    //clang::InputKind inputKind = IK_CXX;
    clang::test a = clang::TUE;
    cout << a << endl;
    //clang::LangOptions languageOptions;
    ////languageOptions.CPlusPlus= 1;
    //clang::CompilerInvocation::setLangDefaults(languageOptions, inputKind);



    return 0;
}
