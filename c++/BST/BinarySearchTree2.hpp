#include <iostream>
#include <string>

using namespace std;

template<typename T>
class TreeNode {
public:
    TreeNode(const T& val):val(val), rChild(0), lChild(0) {}
    ~TreeNode() {
        delete rChild;
        delete lChild;
    }   

     T& getValue() { return val;}
    void setValue( T& _val) { val = _val;}
     TreeNode<T>* getRight() const{ return rChild; }
     TreeNode<T>* getLeft() const{ return lChild; }

    void addChild(TreeNode<T>* treeNode) {
        if(treeNode->getValue() >= val) {
            cout << treeNode->getValue() << ">=" << val << endl; 
            if(rChild == 0) {
                rChild = treeNode;
            } else {
                rChild->addChild(treeNode);
            }   
        } else if(treeNode->getValue() < val) {
            cout << treeNode->getValue() << "<" << val << endl; 
            if(lChild == 0) {
                lChild = treeNode;
            } else {
                lChild->addChild(treeNode);
            }   
        } else {cout << "error!!!!" << treeNode->getValue() << ">=" << val << endl;}   


    }   
    
    T val;
private: 
    TreeNode<T> *rChild;
    TreeNode<T> *lChild;
};

