#include <stdio.h>

int main(int argc, const char *argv[])
{
    parseAndPrintTextFile(argc, argv);

    FILE *fout = fopen("rtl8192cu/BB/Hal8192CUHWImg_BB.c", "a");
    FILE *fin = fopen("rtl8192cu/xx", "r");

    char str[10000];
    
    while (fgets(str, 10000, fin))
        fputs(str, fout) == EOF;

    fclose(fin);
    fclose(fout);

    return 0;
}

