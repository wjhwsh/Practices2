all:
	bison -y -d smallcc.y
	flex smallcc.l
	gcc -c y.tab.c lex.yy.c
	gcc y.tab.o lex.yy.o -o smallcc.out
clean:
	rm -rf *.o y.tab.* lex.yy.c *.out
