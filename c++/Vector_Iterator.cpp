#include <iostream>
#include <vector>

using namespace std;

typedef struct {
    int number;
    string name;
} Entry;

int main(int argc, char **argv)
{
    Entry e;
    Entry array[2] = {{1, "one"}, {2, "two"}};

    for(int i = 0; i < 2; i++) {
        cout << "print Structure: " << endl;
        cout << "number: " << array[i].number << "name: " << array[i].name << endl;
    }

    cout << endl;

    vector<Entry> array_v(array, array + 2);

    for(vector<Entry>::iterator it = array_v.begin(); it != array_v.end(); it++) {
        cout << "print Vector: " << endl;
        cout << "number: " << (*it).number << "name: " << (*it).name << endl;
    }

    return 0;
}
