// insert_iterator example
#include <iostream>
#include <iterator>
#include <list>
using namespace std;

int main () {
  list<int> firstlist, secondlist;
  for (int i=1; i<=5; i++)
  { firstlist.push_back(i); secondlist.push_back(i*10); }

  list<int>::iterator it;
  it = firstlist.begin(); advance (it,3);

  insert_iterator< list<int> > insert_it (firstlist,it);

  copy (secondlist.begin(),secondlist.end(),insert_it);

  for ( it = firstlist.begin(); it!= firstlist.end(); ++it )
      cout << *it << " ";
  cout << endl;

  return 0;
}
