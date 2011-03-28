def print_two(s):
    print s,
    print s,
def print_four(s):
    print_two(s);
    print_two(s);
def do_two(func, size):
    if(size == 0):
        func();
        func();
    else:
        func(size);
        func(size);
def do_four(func, size):
    do_two(func, size);
    do_two(func, size);
#---------------------------------------------------------------
def addOneCol_bound():
    print_four("-");
    print "+",
def addOneCol_normal():
    print_four(" ");
    print "|",
def printOneNormal(size):#|   |   |
    if(size == 2):
        print "|",
        do_two(addOneCol_normal, 0);
        print
    elif(size == 4):
        print "|",
        do_four(addOneCol_normal, 0);
        print
def printOneRowElement(size): #|  |  |*4
    do_four(printOneNormal, size);
def addOneRowEntity(size): #u-shape
    printOneRowElement(size);
    printOneBound(size);
def printOneBound(size): #+---+---+
    print "+",
    if(size == 2):
        do_two(addOneCol_bound, 0);
        print
    elif(size == 4):
        do_four(addOneCol_bound, 0);
        print
def print_grid(size):
    printOneBound(size);
    do_four(addOneRowEntity, size);    

size = int(raw_input("Please enter the size AxA rectangle: A="));
print_grid(size);
