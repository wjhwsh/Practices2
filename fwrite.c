#include <stdio.h>
#include <fcntl.h>
#define fileno(p) ((p)->_file)

int main(int argc, char** argv)
{
    FILE* fp; 
    char* obuf = "哈囉世界";
    char* ibuf[100];
    //write
    fp = fopen("input.txt", "w");
    if(fwrite(obuf, (sizeof(char)*3)*4+1, 1, fp) == 0)
        printf("fwrite failed!");
    else
        printf("File Handle: %d, Size of Buffer: %d, Return Value: %d\n", fp, (sizeof(char)*3)*4+1, fp);  
    fclose(fp);
    //read
    fp = fopen("input.txt", "r");
    if(fread(ibuf, 1, (sizeof(char)*3)*4+1, fp) == 0)
        printf("fread failed!");
    else
        printf("iutput Buffer: %s\n", ibuf);
    fclose(fp);
    
    int fd = open("input.txt", O_RDONLY);
    printf("File Descriptor: %d\n", fd);
    return 0;
}

