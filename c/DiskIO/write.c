#include <stdio.h>

int main(int argc, const char *argv[])
{
    FILE *fin = fopen("hello.txt", "w+");
    const char *str = "你\0好嗎很";

    printf("%lu", sizeof(str));

    //fwrite(str+3, 1, 4, fin);
    //fwrite(str, 1, 4, fin);
    //fwrite(str+9, 1, 4, fin);
    //fwrite(str+6, 1, 4, fin);
    fwrite(str, 12, 1, fin);

    fclose(fin);
    
    return 0;
}
