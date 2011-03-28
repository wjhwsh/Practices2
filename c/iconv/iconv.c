#include <iconv.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    iconv_t iconv_handle;         /* Conversion Descriptor returned       */
    /* from iconv_open() function           */
    char ibuf[19];
    char* obuf;                   /* Buffer for converted characters      */
    size_t ibuflen;               /* Length of input buffer               */
    size_t obuflen;               /* Length of output buffer              */
    char *isav;                   /* Saved pointer to input buffer        */
    char *osav;                   /* Saved pointer to output buffer       */

    //read text from file
    FILE* fp;
    fp = fopen("xxx.big5", "r");
    fread(ibuf, 19, 1, fp); 
    fclose(fp);


    iconv_handle = iconv_open("utf-8","big5");

    if (0)
    {
        perror("ERROR");
        printf("iconv_open fail: %d\n",errno);
        exit(-1);
    }
    else
    {
        ibuflen = strlen(ibuf);
        obuflen = ibuflen;
        obuf    = (char *) malloc(obuflen);
        /* Save pointers to input and output buffers as these are modified by iconv()*/
        /* function                                                                  */
        isav    = ibuf;
        osav    = obuf;
        printf("inbuf = %s\n",ibuf);
        iconv(iconv_handle, &ibuf, &ibuflen, &obuf, &obuflen);

        //write text into file
        FILE* fp2;
        fp2 = fopen("xxx.utf8", "w");
        fwrite(obuf, 19, 1, fp2);
        fclose(fp2);

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
        printf("outbuf  7 = %x\n",osav[7]);
        printf("outbuf  8 = %x\n",osav[8]);
        printf("outbuf  9 = %x\n",osav[9]);
        printf("outbuf 10 = %x\n",osav[10]);

        iconv_close(iconv_handle);
    }
    return(0);
}