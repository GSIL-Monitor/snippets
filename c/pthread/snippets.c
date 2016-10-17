#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

void * hello()
{
	pthread_setcancelstate(0, NULL);
	for(;;) {
		usleep(100000);
		printf("Hello world!\n");
	}
	pthread_exit(NULL);
}


int main(int argc, char** argv)
{
	pthread_t p;
	pthread_create(&p, NULL, hello, NULL);
	void **p_exit = NULL;
	for (int i = 0; i < 2; i ++) {
		sleep(1);

	}
	pthread_cancel(p);
	pthread_join(p, p_exit);
	pthread_exit(NULL);
	return 0;
}
