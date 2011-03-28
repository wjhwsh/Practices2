import os.path
if os.path.exists("metadata.txt"):
    print "found"
    fin = open('metadata.txt', 'r+')
    str = fin.read()
    list = str.split(' ')
    print list
else:
    print "not found"
    fin = open('metadata.txt', 'w')
    fin.write("apple banana")

list.append("cisco")
fin.write(' '.join(list))
fin.close()
