#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <sched.h>
#include <linux/unistd.h>
#include <sys/syscall.h>
#include <errno.h>

#define INC_TO 1000000 // one million...

int global_int = 0;
pthread_spinlock_t spinlock;

pid_t gettid( void )
{
    return syscall( __NR_gettid );
}

void *thread_routine( void *arg )
{
    int i;
    int proc_num = (int)(long)arg;
    cpu_set_t set;

    CPU_ZERO( &set );
    CPU_SET( proc_num, &set );

    if (sched_setaffinity( gettid(), sizeof( cpu_set_t ), &set ))
    {
        perror( "sched_setaffinity" );
        return NULL;
    }

        pthread_spin_lock(&spinlock);
    for (i = 0; i < INC_TO; i++)
    {
        global_int++;
//        __sync_add_and_fetch( &global_int, 1 );
    }
        pthread_spin_unlock(&spinlock);

    return NULL;
}

int main()
{
    int procs = 0;
    int i, pshared;
    pthread_t *thrs;

    // Getting number of CPUs
    procs = (int)sysconf( _SC_NPROCESSORS_ONLN );
    if (procs < 0)
    {
        perror( "sysconf" );
        return -1;
    }

    thrs = malloc( sizeof( pthread_t ) * procs );
    
    if (thrs == NULL)
    {
        perror( "malloc" );
        return -1;
    }

    printf( "Starting %d threads...\n", procs );

    for (i = 0; i < procs; i++)
    {
        if (pthread_create( &thrs[i], NULL, thread_routine,
            (void *)(long)i ))
        {
            perror( "pthread_create" );
            procs = i;
            break;
        }
        if (pthread_spin_init(&spinlock, pshared))
        {
            perror( "pthread_spinlock failed" );
            break;
        }
    }

    for (i = 0; i < procs; i++)
        pthread_join( thrs[i], NULL );

    free( thrs );

    printf( "After doing all the math, global_int value is: %d\n",
        global_int );
    printf( "Expected value is: %d\n", INC_TO * procs );

    return 0;
}
