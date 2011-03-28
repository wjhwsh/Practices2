#include <iostream>
#include <vector>
//#include "BinarySearchTree.hpp"
#include "BinarySearchTree2.hpp"

using namespace std;

TreeNode<int> *root = new TreeNode<int>(7);
TreeNode<int> *nodeArray[11];

void InOrder(TreeNode<int>* node)
{
    if(node == NULL)
        return;
    //cout << "The value of current node: " << node->getValue() << endl;
    if(node->getRight()==NULL && node->getLeft() == NULL) {
        cout << node->getValue() << ", ";
        return;
    } 
    InOrder(node->getLeft());
    cout << node->getValue() << ", ";  
    
    InOrder(node->getRight());
}

int main(int argc, char **argv)
{
    int node[11] = { 2, 12, 1, 6, 3, 4, 5, 8, 11, 10, 9 };
    for(int i = 0; i < 11; i++) {                                   
        nodeArray[i] = new TreeNode<int>(node[i]);
        root->addChild(nodeArray[i]);
    }
    //const TreeNode<string> *a = root.getRight();
    //const TreeNode<string> *b = const_cast<TreeNode<string>*>(a)->getRight(); // why it must use const_cast?

    //in-order traversal
    InOrder(root);

    return 0;
}


