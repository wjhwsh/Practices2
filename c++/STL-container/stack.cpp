#include <iostream>
#include <vector>
using namespace std;

template <class T>
class Stack {
    vector<T> s;
    typename vector<T>::iterator it;
    int tos;
    
public:
    Stack(int size) {
        tos = 0;
    }
    bool isEmpty();
    T pop();
    void push(T element);
};

template <class T>
bool Stack<T>::isEmpty() {
    return (tos == 0) ? true : false;
}
template <class T>
T Stack<T>::pop() {
    T tmp = s[--tos];
    s.pop_back();
    //for (it = s.begin(); it != s.end(); ++it)
    //    cout << *it << "\t";
    //cout << endl;
    return tmp;
}
template <class T>
void Stack<T>::push(T element) {
    tos++;
    s.push_back(element);
}

int main(int argc, char **argv) 
{
    Stack<int> s(1);
    s.push(1);
    s.push(2);
    cout << s.pop() << endl;
    cout << s.pop() << endl;

    s.push(1);
    s.push(2);
    cout << s.pop() << endl;
    s.push(3);
    cout << s.pop() << endl;
    cout << s.pop() << endl;
    return 0;
}
