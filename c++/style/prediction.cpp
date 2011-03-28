// version 1  
bool FoundFoo = false;
for (unsigned i = 0, e = BarList.size(); i != e; ++i)
  if (BarList[i]->isFoo()) {
    FoundFoo = true;
    break;
  }
  
if (FoundFoo) {
  ...
}

// version 2
static bool ListContainsFoo(const std::vector<Bar*> &List) {
  for (unsigned i = 0, e = List.size(); i != e; ++i)
    if (List[i]->isFoo())
      return true;
  return false;
}
...

if (ListContainsFoo(BarList)) {
  ...
}
