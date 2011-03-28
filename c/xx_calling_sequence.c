#include <stdio.h>
int hi(int a, int b) {
        int t = a+b;
        return t;
}
int main(int argc, char *argv[]) {
        hi(1, 2);
        return 0;
}
//http://en.wikipedia.org/wiki/X86
//rbp: frame pointer register
//rsp: stack pointer register
//edi: extended destination index register
//esi: extended source index register
