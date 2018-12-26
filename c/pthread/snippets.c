#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

static int a1 = 0;
static int a2 = 0;

void * hello1()
{
	pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
	while (1) {
		a1++;
		// usleep(1);
	}
	// for (int i = 0; i < 10; i++)
	// for(;;) {
	// 	usleep(100000);
	// 	printf("Hello world!\n");
	// }
	pthread_exit(NULL);
}

void * hello2()
{
	pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
	while (1) {
		a2++;
		// usleep(1);
	}
	// for (int i = 0; i < 10; i++)
	// for(;;) {
	// 	usleep(100000);
	// 	printf("Hello world!\n");
	// }
	pthread_exit(NULL);
}


int main(int argc, char** argv)
{

	printf("const: %d\n", PTHREAD_CANCEL_ENABLE);
	pthread_t p1, p2;

	pthread_create(&p1, NULL, hello1, NULL);
	pthread_create(&p2, NULL, hello2, NULL);
	void **p_exit = NULL;

	struct timespec tstart={0,0}, tend={0,0};
	clock_gettime(CLOCK_MONOTONIC, &tstart);

	for (int i = 0; i < 2; i ++) {
		sleep(1);
	}
	pthread_cancel(p1);
	pthread_cancel(p2);
	pthread_join(p1, p_exit);
	pthread_join(p2, p_exit);


    clock_gettime(CLOCK_MONOTONIC, &tend);
    printf("took about %.5f seconds\n",
           ((double)tend.tv_sec + 1.0e-9*tend.tv_nsec) -
           ((double)tstart.tv_sec + 1.0e-9*tstart.tv_nsec));

	printf("a1: %d\n", a1);
	printf("a2: %d\n", a2);

	pthread_exit(NULL);
	return 0;
}
