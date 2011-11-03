#include <stdio.h>
#include <stdlib.h>

int main(int argc, const char *argv[])
{
    FILE *fin = fopen("hello.txt", "r+");
    char *str = (char*)malloc(sizeof(char) * 12);

    fread(str+3, 1, 4, fin);
    fread(str, 1, 4, fin);
    fread(str+9, 1, 4, fin);
    fread(str+6, 1, 4, fin);

    FILE *fout = fopen("hello.ok.txt", "w+");
    fwrite(str, 12, 1, fout);

    fclose(fin);
    fclose(fout);
    
    return 0;
}
