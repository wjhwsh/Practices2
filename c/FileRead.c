#include <stdio.h>

int main(int argc, char **argv)
{
    FILE *fp = fopen("/Users/kordan/Desktop/dic_list.txt", "r");
    char cInput;
    if(fp == NULL) {
        printf("Not Found\n"); 
        return 0;
    }
    while((cInput = fgetc(fp)) != EOF) {
        printf("%c", cInput);

    }
    fclose(fp);
    return 0;
}
