//AST/Type.cpp
#include "Type.h"
using namespace clang;
bool QualType::isEqualWith(QualType T, int x) {
    if (T.count == x)
        return true;
    return false;
}
