from array import array
class ClassA:
    def __init__(self):
        print 'Hello'
        
a = array('i')
a.append(1)
a.append(2)
a.append(3)
a.append(4)
print a.count(1) 


