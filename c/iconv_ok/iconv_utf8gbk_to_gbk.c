#include <iconv.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    iconv_t iconv_handle1;         /* Conversion Descriptor returned       */
    /* from iconv_open() function           */
    char* ibuf = (char *)malloc(7);
    char* obuf;                   /* Buffer for converted characters      */
    size_t ibuflen;               /* Length of input buffer               */
    size_t obuflen;               /* Length of output buffer              */
    char *isav;                   /* Saved pointer to input buffer        */
    char *osav;                   /* Saved pointer to output buffer       */

    //read text from file
    FILE* fp;
    fp = fopen("test.gbk.utf8.txt", "r");
    fread(ibuf, 7, 1, fp); 
    fclose(fp);


    iconv_handle1 = iconv_open("gbk","utf-8");

    if (0)
    {
        perror("ERROR");
        printf("iconv_open fail: %d\n",errno);
        exit(-1);
    }
    else
    {
        ibuflen = 7;
        obuflen = 5;
        obuf    = (char *) malloc(obuflen);
        /* Save pointers to input and output buffers as these are modified by iconv()*/
        /* function                                                                  */
        isav    = ibuf;
        osav    = obuf;
        iconv(iconv_handle1, &ibuf, &ibuflen, &obuf, &obuflen);
        printf("ibuflen:%d obuflen:%d", ibuflen, obuflen);
        ibuf = isav;
        obuf = osav;
        FILE* fp3;
        fp3 = fopen("test.gbk.txt", "w");
        fwrite(obuf, 5, 1, fp3);
        fclose(fp3);

        printf("outbuf = %s\n",osav);

        /* Also print each character in hexadecimal to check the conversion          */
        /* The hex values can be compared with the values for code page 00850.       */

        printf("outbuf  0 = %x\n",osav[0]);
        printf("outbuf  1 = %x\n",osav[1]);
        printf("outbuf  2 = %x\n",osav[2]);
        printf("outbuf  3 = %x\n",osav[3]);
        printf("outbuf  4 = %x\n",osav[4]);
        printf("outbuf  5 = %x\n",osav[5]);
        printf("outbuf  6 = %x\n",osav[6]);

        iconv_close(iconv_handle1);
    }
    return(0);
}
