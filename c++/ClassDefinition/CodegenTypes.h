#include <iostream>
#include "Type.h"

//Codegen/CodegenTypes.h
namespace clang {
    //class QualType;

    QualType a;
    void print() { if (a.isEqualWith(0)) std::cout << "hello" << std::endl; }
}
