#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#define MAX1 5
#define MAX2 10

pthread_t thread[2];
pthread_mutex_t mut;
int number=0, i;

void *thread1()
{
        printf ("thread1 : I'm thread 1\n");
        for (i = 0; i < MAX1; i++)
        {
                printf("thread [1] : number = %d  i=%d\n", number,i);
                pthread_mutex_lock(&mut);
                        number++;
                pthread_mutex_unlock(&mut);
                sleep(2);
        }

        printf("thread1 :Is main function waiting for me acomplishing task? \n");
        pthread_exit(NULL);
}
void *thread2()
{
        printf("thread2 : I'm thread 2\n");
        for (i = 0; i < MAX2; i++)
        {
                printf("thread [2] : number = %d  i=%d\n", number,i);
                pthread_mutex_lock(&mut);
                        number++;
                pthread_mutex_unlock(&mut);
                sleep(3);
        }

        printf("thread2 :Is main function waiting for me  to acomplish task ?\n");
        pthread_exit(NULL);
}
void thread_create(void)
{
        int temp;
        memset(&thread, 0, sizeof(thread));          //comment1
        /*創建線程*/
        if((temp = pthread_create(&thread[0], NULL, thread1, NULL)) != 0)       //comment2
                printf("線程1創建失敗!\n");
        else
                printf("Thread 1 is established\n");
        if((temp = pthread_create(&thread[1], NULL, thread2, NULL)) != 0)  //comment3
                printf("線程2創建失敗");
        else
                printf("Thread 2 is established\n");
}
void thread_wait(void)
{
        /*等待線程結束*/
        if(thread[0] !=0) {                   //comment4
                pthread_join(thread[0],NULL);
                printf("Thread 1 is over \n");
        }
        if(thread[1] !=0) {                //comment5
                pthread_join(thread[1],NULL);
                printf("Thread 2 is over\n");
        }
}

int main()
{
        /*用默認屬性初始化互斥鎖*/
        pthread_mutex_init(&mut,NULL);
        printf("I am the main funtion,and I am establishing threads. Ha-ha\n");
        thread_create();
        printf("I am the main funtion,and I am waiting for thread to accomplish task. Ha-ha\n");
        thread_wait();
        return 0;
}

