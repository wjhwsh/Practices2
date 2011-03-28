//include/AST/Type.h

namespace clang {
    class QualType {
    public:
        QualType() { count = 0; }

        int count;

        bool isEqualWith(int c) const {
                // A constant block would do this instead:
                //
                // return this->isEqualWith(*this, c);
                //
                // so, it must have a static qualifier in line 20.
                return QualType::isEqualWith(*this, c);
        }

    private:
        static bool isEqualWith(QualType T, int x);
    };
};
