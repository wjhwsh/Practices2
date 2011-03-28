def has_match(t1,t2):
    for x,y in zip(t1,t2):
        print '(x, y) is (%s,%s)' %(x, y)
        if x==y:
            print '%s is equal to %s' %(x, y)
    print '%s xxxx %s' %(x, y)

has_match(('aabbcc'),('ccbbaa'))

