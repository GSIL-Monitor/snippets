#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

void * hello()
{
	usleep(1000);
	printf("Hello world!\n");
	pthread_exit(NULL);
}


int main(int argc, char** argv)
{

	for (;;) {
		pthread_t p;
		void **p_exit = NULL;
		pthread_create(&p, NULL, hello, NULL);
		sleep(1);
		pthread_join(p, p_exit);
	}

	pthread_exit(NULL);
	return 0;
}
