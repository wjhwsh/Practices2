#include <iconv.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    char f_code[33];              /* From CCSID                           */
    char t_code[33];              /* To CCSID                             */
    iconv_t iconv_handle;         /* Conversion Descriptor returned       */
    /* from iconv_open() function           */
    char *ibuf = "國家";   /* Buffer of characters to be converted */
    char *obuf;                   /* Buffer for converted characters      */
    size_t ibuflen;               /* Length of input buffer               */
    size_t obuflen;               /* Length of output buffer              */
    char *isav;                   /* Saved pointer to input buffer        */
    char *osav;                   /* Saved pointer to output buffer       */

    /* All reserved positions of from code (last 12 characters) and to code   */
    /* (last 19 characters) must be set to hexadecimal zeros.                 */

    memset(f_code,'\0',33);
    memset(t_code,'\0',33);

    strcpy(f_code,"IBMCCSID000370000000");
    strcpy(t_code,"IBMCCSID00850");

    iconv_handle = iconv_open("big5","utf-8");
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
        perror("ERROR");
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
