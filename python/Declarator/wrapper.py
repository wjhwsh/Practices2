enable_tracing = True 
if enable_tracing:
    debug_log = open("debug.log","w")

def trace(func): 
    if enable_tracing:
        def callf(*args,**kwargs): 
            debug_log.write("Calling %s: %s, %s\n" % (func.__name__, args, kwargs)) 
            r = func(*args,**kwargs)
            debug_log.write("%s returned %s\n" % (func.__name__, r))
            return r 
        return callf
    else: 
        return func
@trace
def print_func(str1, str2, str3, str4):
    return_val = 0
    print str1
    return return_val
print_func('Hello1', 'Hello2', 'Hello3', 'Hello4')
