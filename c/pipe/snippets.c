#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#include "util/util.h"


#define PROG_LENGTH 2


void get_current_time(char *format, char* output, int length)
{
	char buf[length];
	memset(buf, 0, length);
	time_t now = time(NULL);
	strftime(buf, length, format, localtime(&now));
	strncat(output, buf, length);
}

void read_output(int fd, const char* prefix) {
	char now[9] = {0};
	char buf[4096] = {0};
	int f = 0;

	for (;;) {
		f = readline(fd, buf, sizeof(buf));
		/* printf("[parent] %d\n", f); */
		switch(f) {
		case 0:
			/* end */
			return;
			break;
		case -1:
			usleep(100000);
			return;
		default:
			;

			if (strlen(buf) <= 0) return;

			get_current_time("%H:%M:%S", now, sizeof(now));

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
}


void run_child(const char* command, int* rv_pid, int* rv_fd)
{
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
			  command,
			  (char *) 0);
		perror("exec error");
		exit(-1);

	case -1:
		perror("fork error");

	default:
		/* parent */
		close(fd[1]);
 		int flags = fcntl(fd[0], F_GETFL, 0);
		fcntl(fd[0], F_SETFL, flags | O_NONBLOCK);
		break;
	}

	*rv_pid = pid;
	*rv_fd = fd[0];
}



int main(int argc, char** argv)
{

	char cmd1[] = "while true; do date; sleep 2; done";
	/* char cmd2[] = "while true; do date +%s; sleep 3; done"; */
	char cmd2[] = "echo 1";

	char* programs[2];

	programs[0] = cmd1;
	programs[1] = cmd2;

	char* prefix[PROG_LENGTH];
	prefix[0] = " worker1 | ";
	prefix[1] = " worker2 | ";

	int fds[PROG_LENGTH];
	int pids[PROG_LENGTH];

	int alive_progs = PROG_LENGTH;

	for(int _ = 0; _ < PROG_LENGTH; _++){
		int fd = 0;
		int pid = 0;
		run_child(programs[_], &pid, &fd);
		fds[_] = fd;
		pids[_] = pid;
	}

	for(int _ = 0; _ < PROG_LENGTH; _++) {
		printf("fd: %d\n", fds[_]);
		printf("pid: %d\n", pids[_]);
	}


	for (;;) {

		int curr_alive_progs = alive_progs;
		for(int _ = 0; _ < curr_alive_progs; _++) {
			int p_status = 0;
			pid_t dead_pid = waitpid(0, &p_status, WNOHANG);
			if (dead_pid > 0) {
				printf("[parent] dead child: %u\n", dead_pid);
				int idx = -1;
				for (int _ = 0; _ < curr_alive_progs; _++) {
					if (pids[_] == dead_pid) {
						idx = _;
						break;
					}
				}
				fds[idx] = 0;
			}
		}

		fd_set readfds;
		FD_ZERO(&readfds);

		for(int _ = 0; _ < PROG_LENGTH; _++) {

			printf("[parent] ");

			if (fds[_] > 0) {
				FD_SET(fds[_], &readfds);
			}
		}

		/* printf("[parent] about to select\n"); */
		int rc = select(
			fds[PROG_LENGTH-1] + 1,
			&readfds,
			NULL,
			NULL,
			NULL);
		if (rc == -1) continue;

		for(int _ = 0; _ < PROG_LENGTH; _++) {
			if (FD_ISSET(fds[_], &readfds)) {
				printf("[parent] ready index: %d, fd: %d\n",
					   _,
					   fds[_]);
				read_output(fds[_], prefix[_]);
				printf("[parent] read complete\n");
			}
		}


	}
}
