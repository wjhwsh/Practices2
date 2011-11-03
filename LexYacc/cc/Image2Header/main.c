#include <stdio.h>
#include "main.h"

int main(int argc, const char *argv[])
{
    if (argc > 2) {
        char *chip_id = argv[1];
        if (parseTextAndPrintArrayToFile(chip_id, eFileType) == NULL)
            fprintf(stderror, "Fail to load and parse the text file.\n");

        FILE *fout = fopen("rtl8192cu/BB/Hal8192CUHWImg_BB.c", "a");
        FILE *fin = fopen("rtl8192cu/xx", "r");

        char str[10000];
        
        while (fgets(str, 10000, fin))
            fputs(str, fout) == EOF;

        fclose(fin);
        fclose(fout);

    } else {
        printf("Usage: %s CHIP_ID FILE_TYPE\n", argv[0]);
    
    }

    return 0;
}

