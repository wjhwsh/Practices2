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
def print_func(str):
    print str
print_func = trace(print_func)
print_func('Hello')
