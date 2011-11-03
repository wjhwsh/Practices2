# build environment for cygwin

# bison -d Image2Header.y    produces Image2Header.tab.c
# bison -y -d Image2Header.y produces y.tab.c (the standard yacc output)

INPUT = ./data/input

all:
	bison --verbose --debug -y -d Image2Header.y
	flex Image2Header.l
	gcc -c y.tab.c lex.yy.c main.c
	gcc -Wall y.tab.o lex.yy.o main.o -o Image2Header.out

test:
	./Image2Header.out $(INPUT)

clean:
	rm -rf *.o y.tab.* lex.yy.c *.out
