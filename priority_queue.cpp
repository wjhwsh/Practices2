// constructing priority queues
#include <iostream>
#include <queue>
using namespace std;

class mycomparison
{
  bool reverse;
public:
  mycomparison(const bool& revparam=false)
    {reverse=revparam;}
  bool operator() (const int& lhs, const int&rhs) const
  {
    if (reverse) return (lhs>rhs);
    else return (lhs<rhs);
  }
};

int main ()
{
  int myints[]= {3,4,1,2};
  typedef priority_queue<int,vector<int>,mycomparison> mypq_type;
  mypq_type mypq (myints,myints+3,mycomparison(true));

  mypq.push(6);
  mypq.push(5);
  mypq.push(7);
  mypq.push(8);

  cout << "Popping out elements...";
  while (!mypq.empty())
  {
     cout << " " << mypq.top();
     mypq.pop();
  }
  cout << endl;

  return 0;
}


