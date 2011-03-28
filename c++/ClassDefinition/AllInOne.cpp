//include/AST/Type.h

namespace clang {
    class QualType {
    public:
        QualType() { count = 0; }

        int count;

        bool isEqualWith(int c) const {
                return QualType::isEqualWith(*this, c);
        }


    private:
        static bool isEqualWith(QualType T, int x);
    };
};

//------------------------------------------------------------------------------------------
//AST/Type.cpp
using namespace clang;
bool QualType::isEqualWith(QualType T, int x) {
    if (T.count == x)
        return true;
    return false;
}

//------------------------------------------------------------------------------------------
//Codegen/CodegenTypes.h
#include <iostream>
namespace clang {
    class QualType;

    QualType a;
    void print() { if (a.isEqualWith(0)) std::cout << "hello" << std::endl; }
}

//------------------------------------------------------------------------------------------
//Codegen/CodegenTypes.cpp
using namespace clang;

int main(int argc, char **argv) {

    print();
    
    return 0;
}
