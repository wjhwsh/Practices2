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

    const T& getValue() { return val;}
    void setValue(const T& _val) { val = _val;}
    const TreeNode<T>* getRight() { return rChild; }
    const TreeNode<T>* getLeft() { return lChild; }

    void addChild(TreeNode<T>* treeNode) {
        if(treeNode->getValue() >= val) {
            if(rChild == 0) {
                rChild = treeNode;
            } else {
                rChild->addChild(treeNode);
            }   
        } else {
            if(lChild == 0) {
                lChild = treeNode;
            } else {
                lChild->addChild(treeNode);
            }   
        }   

    }   
    
    T val;
private: 
    TreeNode<T> *rChild;
    TreeNode<T> *lChild;
};

