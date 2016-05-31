#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>


void signal_handler(int sig)
{
	if (sig == SIGHUP) {
		printf("HUP!\n");
	}
	if (sig == SIGINT) {
		printf("INT!\n");
	}
	if (sig == SIGQUIT) {
		printf("QUIT!\n");
	}
}


int main(int argc, char** argv)
{

	struct sigaction sa;

	sa.sa_handler = &signal_handler;
	sa.sa_flags = SA_RESTART;
	sigfillset(&sa.sa_mask);

	sigaction(SIGINT, &sa, NULL);
	sigaction(SIGHUP, &sa, NULL);
	sigaction(SIGQUIT, &sa, NULL);

	while (1)
		sleep(1);

	return 0;
}
