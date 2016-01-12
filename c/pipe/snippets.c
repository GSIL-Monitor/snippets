#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#include "util/util.h"



void get_current_time(char *format, char* output, int length)
{
	char buf[length];
	memset(buf, 0, length);
	time_t now = time(NULL);
	strftime(buf, length, format, localtime(&now));
	strncat(output, buf, length);
}



int main(int argc, char** argv)
{

	char cmd1[] = "while true; do date; sleep 2; done";
	char cmd2[] = "while true; do date; sleep 3; done";

	char* programs[2];

	programs[0] = cmd1;
	programs[1] = cmd2;

	int fd[2];
	if (pipe(fd) == -1) perror("pipe error");
	pid_t pid = fork();

	switch (pid) {
	case 0:
		/* child */

		dup2(fd[1], 1);
		dup2(fd[1], 2);
		close(fd[0]);
		close(fd[1]);

		execl("/bin/bash",
					"bash",
					"-c",
					"while true; do date; sleep 1; done",
					(char *) 0);
		perror("exec error");
		exit(-1);

	case -1:
		perror("fork error");
		break;

	default:
		/* parent */
		close(fd[1]);

		/* printf("[parent] child input fd: %d\n", fd[1]); */

 		int flags = fcntl(fd[0], F_GETFL, 0);
		fcntl(fd[0], F_SETFL, flags | O_NONBLOCK);

		char now[9] = {0};
		char buf[4096] = {0};
		int f = 0;

		for (;;) {
			fd_set readfds;
			FD_ZERO(&readfds);
			FD_SET(fd[0], &readfds);

			/* printf("[parent] about to select\n"); */
			int rc = select(fd[0] + 1, &readfds, NULL, NULL, NULL);
			if (rc == -1) continue;
			if (FD_ISSET(fd[0], &readfds)) {

				for (;;) {
					f = readline(fd[0], buf, sizeof(buf));
					/* printf("[parent] %d\n", f); */
					switch(f) {
					case 0:
						/* end */
						break;
					case -1:
						usleep(100000);
						goto out;
						break;
					default:
						;

						if (strlen(buf) <= 0) goto out;

						get_current_time("%H:%M:%S", now, sizeof(now));

						char prefix[] = " worker1 | ";

						size_t s = strlen(now)
							+ strlen(prefix) + strlen(buf);

						char out[s];
						memset(out, 0, s);

						strcat(out, now);
						strcat(out, prefix);
						strcat(out, buf);
						printf("%s", out);

						break;
					}
					memset(now, 0, sizeof(now));
				}

out:
				continue;

			}
		}

		break;




		break;
	}
	return 0;
}
