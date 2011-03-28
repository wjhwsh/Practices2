#include <stdio.h>

char const ActivityName[] = "2010 NTU CSIE 新生盃程式解題競賽";
char const ActivityTime[] = "2010 / 12 / 19 (日)";
char const Important[] = "三人一組、寫程式、吃點心、拿氣球";

char const Details[] = "詳情請按下 PageDown ...";

char const *QUINE[100], **a = QUINE, **b = QUINE; int main() {
#define B(x) x; *b++ = "B(" #x ")";
#define A(x) while(a<b)puts(*a++); puts("A(" #x ")"); x;
B(puts("#include <stdio.h>\n"))
B(puts("char const ActivityName[] = \"2010 NTU CSIE 新生盃程式解題競賽\";"))
B(puts("char const ActivityTime[] = \"2010 / 12 / 19 (日)\";"))
B(puts("char const Important[] = \"三人一組、寫程式、吃點心、拿氣球\";\n"))
B(puts("char const Details[] = \"詳情請按下 PageDown ...\";\n"))
B(puts("char const *QUINE[100], **a = QUINE, **b = QUINE; int main() {"))
B(puts("#define B(x) x; *b++ = \"B(\" #x \")\";"))
B(puts("#define A(x) while(a<b)puts(*a++); puts(\"A(\" #x \")\"); x;"))
A(puts("}"); return 0)
}
