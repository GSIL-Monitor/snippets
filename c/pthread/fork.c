#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>


void * fork_master()
{
	pid_t pid = fork();
	int ev;
	if (pid < 0) {
		perror("fork error");
	}
	else if (pid == 0) {
		// child

		char ** argv[2];
		char command[] = "/usr/bin/python";
		char file[] = "sleep.py";
		argv[0] = command;

		execlp(
			"/usr/bin/python", "/usr/bin/python",
			"sleep.py", 0);
	}
	else {
		// parent
		while (1) {
			pid_t c = waitpid(-1, &ev, WNOHANG);
			if (c == 0) {
				// still running
				sleep(1);
			}
			else if (c == pid) {
				printf("child has exited\n");
				pthread_exit(NULL);
			}
			else if (c == -1) {
				if (errno == EAGAIN) {
					sleep(1);
					continue;
				}
				else {
					printf("%s\n", strerror(errno));
					pthread_exit(NULL);
				}
			}
		}
	}

	pthread_exit(NULL);
}

int main ()
{
	pthread_t p;
	pthread_create(&p, NULL, fork_master, NULL);

	srand(20);
	int r;

	while (1) {
		r = rand();
		printf("main loop: %d\n", r);
		sleep(1);
	}

}
