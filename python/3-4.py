def print_twice(s):
    print s
    print s
def do_four(func, argument):
    func(argument);
    func(argument);

do_four(print_twice, 'spam')
