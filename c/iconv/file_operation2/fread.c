#include <stdio.h>

int main(int argc, char** argv){
    FILE* fp;
    char buf[19];
    if(argc != 2){
        printf("usage: ./fread file_name\n");
        return 1;
    }
    fp = fopen(argv[1] , "r");
    fread(buf, 19, 1, fp);
    printf("%s\n", buf);
    return 0;
}
