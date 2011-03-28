#include <iconv.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    iconv_t iconv_handle1;         /* Conversion Descriptor returned       */
    iconv_t iconv_handle2;         /* Conversion Descriptor returned       */
    iconv_t iconv_handle3;         /* Conversion Descriptor returned       */
    /* from iconv_open() function           */
    char* ibuf = (char *)malloc(7);
    char* obuf;                   /* Buffer for converted characters      */
    size_t ibuflen;               /* Length of input buffer               */
    size_t obuflen;               /* Length of output buffer              */
    char *isav;                   /* Saved pointer to input buffer        */
    char *osav;                   /* Saved pointer to output buffer       */

    //read text from file
    FILE* fp;
    fp = fopen("test.gb.utf8.txt", "r");
    fread(ibuf, 7, 1, fp); 
    fclose(fp);


    iconv_handle1 = iconv_open("gbk","utf-8");
    iconv_handle2 = iconv_open("big5","gbk");
    iconv_handle3 = iconv_open("utf-8","big5");

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
        iconv(iconv_handle1, &ibuf, &ibuflen, &obuf, &obuflen);
        ibuf = isav;
        obuf = osav;
        FILE* fp3;
        fp3 = fopen("test.gbk.txt", "w");
        fwrite(obuf, 7, 1, fp3);
        fclose(fp3);

        ibuflen = strlen(ibuf);
        obuflen = ibuflen;
        /* Save pointers to input and output buffers as these are modified by iconv()*/
        /* function                                                                  */
        FILE* fi1;
        fi1 = fopen("test.gbk.txt", "r");
        fread(ibuf, 7, 1, fi1); 
        fclose(fi1);
        iconv(iconv_handle2, &obuf, &obuflen, &ibuf, &ibuflen);
        ibuf = isav;
        obuf = osav;
        FILE* fp4;
        fp4 = fopen("test.big5.txt", "w");
        fwrite(obuf, 7, 1, fp4);
        fclose(fp4);

        ibuflen = strlen(ibuf);
        obuflen = ibuflen;
        /* Save pointers to input and output buffers as these are modified by iconv()*/
        /* function                                                                  */
        FILE* fi2;
        fi2 = fopen("test.big5.txt", "r");
        fread(ibuf, 7, 1, fi2); 
        fclose(fi2);
        printf("inbuf = %s\n",ibuf);
        iconv(iconv_handle3, &ibuf, &ibuflen, &obuf, &obuflen);
        ibuf = isav;
        obuf = osav;
        //write text into file
        FILE* fp2;
        fp2 = fopen("test.big5.utf8.txt", "w");
        fwrite(obuf, 7, 1, fp2);
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

        iconv_close(iconv_handle1);
        iconv_close(iconv_handle2);
        iconv_close(iconv_handle3);
    }
    return(0);
}
