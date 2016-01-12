#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>


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
	int fd[2];
	if (pipe(fd) == -1) perror("pipe error");
	pid_t pid = fork();

	switch (pid) {
	case 0:
		/* child */

		dup2(fd[1], 1);
		close(fd[0]);
		close(fd[1]);

		while (1) {
			/* write(2, "child loop\n", 11); */
			printf("just some random output\n");
			fflush(stdout);
			sleep(1);
		}
		break;
	case -1:
		perror("fork error");
		break;

	default:
		/* parent */
		close(fd[1]);

		printf("[parent] child input fd: %d\n", fd[1]);

		int flags = fcntl(fd[0], F_GETFL, 0);
		fcntl(fd[0], F_SETFL, flags | O_NONBLOCK);

		size_t nbytes = 0;
		char buf[4096] = {0};
		char _out[4096] = {0};
		char now[9] = {0};

		while (1) {
			while ((nbytes = read(fd[0], buf, sizeof(buf))) > 0) {
				if (strlen(buf) > 0) {
					printf("[parent] buf strlen: %lu\n",
								 strlen(buf));

					get_current_time(
						"%H:%M:%S",
						now,
						sizeof(now));

					strcat(_out, now);
					strcat(_out, " worker1 |");
					strcat(_out, buf);

					printf(_out);

					memset(buf, 0, sizeof(buf));
					memset(_out, 0, sizeof(_out));
				}
				else {
					usleep(1000);
				}
			}
		}

		break;
	}
	return 0;
}
