#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#define COUNT 200
#define SPLIT 0.01
#define PI  3.14159265
#define INTERVAL 100

double get_time() {
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec*1000+tv.tv_usec*1.0/1000); /* ms */
}

int main() {
	double busy_span[COUNT]; /* need to modify */
	double idle_span[COUNT];
	int half = INTERVAL/2;
	double radian = 0.0;
	double start_time;
	int i;
	for(i=0; i<COUNT; i++) {
		busy_span[i] = (double)(half + half*sin(PI*radian));
		idle_span[i] = (double)(INTERVAL - busy_span[i]);
		radian += SPLIT;
	}
	i = 0;
	while(1) {
		i %= COUNT;
		start_time = get_time();
		while((get_time()-start_time) <= busy_span[i])
			;
		usleep(idle_span[i]*1000);
		i++;
	}
	return 0;
}
