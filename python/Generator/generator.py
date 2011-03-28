def countdown(num):
    print "Count Down from %d" % num
    while num > 0:
        yield num
        num -= 1
    return
c = countdown(10)
for n in c:
    print n
