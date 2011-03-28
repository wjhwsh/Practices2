# Normal linking
all:      
	gcc main.c addvec.c multvec.c -o normal.out
static:
	gcc -c addvec.c multvec.c
	ar rcs libvector.a addvec.o multvec.o
	gcc main.c libvector.a -o static.out
static2:
	gcc -c addvec.c multvec.c
	ar rcs libvector.a addvec.o multvec.o
	gcc -static main.c -L/Developer/SDKs/MacOSX10.5.sdk/usr/lib libvector.a -o $@.out
link:
	gcc -c main.c multvec.c addvec.c
	ar rcs libmultvec.a multvec.o
	ar rcs libaddvec.a addvec.o
	
clean:
	rm -rf *.o *.a *.out
