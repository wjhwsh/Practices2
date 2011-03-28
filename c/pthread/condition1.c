#include <stdio.h>
#include <pthread.h>

pthread_mutex_t count_lock;
pthread_cond_t count_nonzero;
unsigned count;
pthread_t thread[2];

void *decrement_count() {
    pthread_mutex_lock(&count_lock);

    while(count==0) {
        pthread_cond_wait( &count_nonzero, &count_lock);
        count=count-1;
        printf("Dec: count = %i\n", count);
    } 


    pthread_mutex_unlock(&count_lock);

    return NULL;
}

void *increment_count() {
    pthread_mutex_lock(&count_lock);
    
    if(count == 0)
        pthread_cond_signal(&count_nonzero);
    count = count + 1;
    printf("inc: count = %i\n", count);

    pthread_mutex_unlock(&count_lock);
    
    return NULL;
}

int main(int argc, char ** argv)
{
    void *(*dec_fp)() = decrement_count;
    void *(*inc_fp)() = increment_count;

    pthread_create(&thread[0], NULL, dec_fp, NULL);
    pthread_create(&thread[1], NULL, inc_fp, NULL);
    pthread_join(thread[0], NULL);
    pthread_join(thread[1], NULL);

    return 0;
}
