def is_Triangle(a, b, c):
    isTriangle = a > (b + c)
    if (isTriangle and is_Triangle(b, a, c) and is_Triangle(c, b, a)):
        print "NO"
        return False
    else: 
        print "Yes"
        return True
is_Triangle(int(raw_input("a=")), int(raw_input("b=")), int(raw_input("a=")))
