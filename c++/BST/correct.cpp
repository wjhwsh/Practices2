#include <iostream>
#include <string>

using namespace std;

template<typename T>
class TreeNode {
public:
   TreeNode(const T& val) : val_(val), left_(NULL), right_(NULL) {}
  ~TreeNode( ) {
   }

   const T& getVal( ) const {return(val_);}
   void setVal(const T& val) {val_ = val;}
   void addChild(TreeNode<T>* p) {
      const T& other = p->getVal( );
      if (other > val_)
         if (right_)
            right_->addChild(p);
         else
            right_ = p;
      else
         if (left_)
            left_->addChild(p);
         else
            left_ = p;
   }
   const TreeNode<T>* getLeft( ) {return(left_);}
   const TreeNode<T>* getRight( ) {return(right_);}

private:
   T val_;
   TreeNode<T>* left_;
   TreeNode<T>* right_;
};

int main( ) {

   TreeNode<string> node1("A");
   TreeNode<string> node2("B");
   TreeNode<string> node3("C");

   node1.addChild(&node2);
   node1.addChild(&node3);
}
