#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main(int argc, char **argv)
{
    int array[] = {6, 4, 7, 5, 9, 1, 3, 2, 10, 8};
    vector<int> vec(array, array + sizeof(array)/sizeof(int));
    sort(vec.begin(), vec.end());
    
    for(vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) 
        cout << *it << " ";
    cout << endl;

    int value; 
    cout << "Enter the value you want to find: ";
    cin >> value;
    vector<int>::iterator ito = find(vec.begin(), vec.end(), value);
    if(ito != vec.end()) {
        for(vector<int>::iterator iti = vec.begin(); iti != vec.end(); ++iti) {
            if(*ito == *iti)
                cout << "[" << *iti << "]" << " ";
            else
                cout << *iti << " ";
        }
        cout << endl;
    }
    else
        cout << "not found!!" << endl;

    reverse(vec.begin(), vec.end());
    for(vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) 
        cout << *it << " ";
    cout << endl;

    return 0;
}
