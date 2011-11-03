#include <iostream>
#include <cstdio>
#include <signal.h>
#include <pthread.h>

using namespace std;

pthread_t p1, p2;
pthread_attr_t p1_attr, p2_attr;

void *foo(void *arg) {
    const char *c = (const char*)arg;
    while(1) {
        printf("%s\n", c);
        sleep(1);
    }
}

int main(int argc, const char *argv[])
{
    const char *c1 = "p11111111111";
    const char *c2 = "p22222222222";
    void *arg1 = &c1;
    void *arg2 = &c2;

    pthread_attr_init(&p1_attr);
    pthread_attr_init(&p2_attr);
    pthread_create(&p1, &p1_attr, foo, arg1);
    pthread_create(&p2, &p2_attr, foo, arg2);

    while(1) ;
    
    return 0;
}
