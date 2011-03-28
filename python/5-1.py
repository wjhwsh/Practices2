def check_fermat(a, b, c, n):
    if(a**n + b**n == c**n) and n >2: 
        print "Holy smokes, Fermat was wrong!"
    elif n <= 2: 
        print "n must be greater than 2"
    else: 
        print "No, that doesn't work."
    print "a^n + b^n :%d   c^n : %d" %(a**n + b**n, c**n)

check_fermat(int(raw_input("a = ")),int(raw_input("b = ")), int(raw_input("c = ")), int(raw_input("n = ")));
