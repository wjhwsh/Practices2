#include <stdio.h>
#include <string.h>

int main(int argc, char** argv)
{   
    FILE* fp;
    char buf[19];
    strcpy((char *)buf, (const char *)argv[2]);
    if(argc != 3){
        printf("usage: ./fwrite file_name context\n");
        return 1;
    }
    fp = fopen(argv[1], "w+");
    fwrite(buf, 19, 1, fp);
    return 0;
}
