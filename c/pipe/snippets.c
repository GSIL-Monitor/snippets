#include "errno.h"
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/select.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#include "util/util.h"


#define PROG_LENGTH 2

#define ANSI_COLOR_YELLOW "\x1b[1;33m"
#define ANSI_COLOR_BLUE "\x1b[1;34m"
#define ANSI_COLOR_MAGENTA "\x1b[1;35m"
#define ANSI_COLOR_CYAN "\x1b[1;36m"
#define ANSI_COLOR_WHITE "\x1b[1;37m"
#define ANSI_COLOR_RESET "\x1b[0m"
#define EPOLL_QUEUE_LEN 300
#define MAXEVENTS 50


static char* colors[] = {
	ANSI_COLOR_YELLOW,
	ANSI_COLOR_BLUE,
	ANSI_COLOR_MAGENTA,
	ANSI_COLOR_CYAN,
	ANSI_COLOR_WHITE
};

static int breaking = 1;
static int progs = PROG_LENGTH;

void select_ioloop(int pids[], int fds[], char * prefix[]);
void epoll_ioloop(int pids[], int fds[], char * prefix[]);

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
			// usleep(100000);
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

void kill_children(size_t size, int pids[])
{
	for (unsigned int _ = 0; _ < size; _++) {
		if (pids[_] == 0) continue;
		kill(pids[_], SIGTERM);
		printf("[parent] killed: %d\n", pids[_]);
	}

	int p_status;
	for (;;) {
		pid_t dead_pid = waitpid(0, &p_status, WNOHANG);
		if (dead_pid == -1) {
			if (errno == ECHILD) {
				exit(-1);
			}
		}
	}
}

int reap_children(size_t size, int pids[], int fds[])
{
	for(unsigned int _ = 0; _ < size; _++) {
		int p_status = 0;
		pid_t dead_pid = waitpid(0, &p_status, WNOHANG);
		printf("[parent] dead_pid: %d\n", dead_pid);
		if (dead_pid == 0) continue;

		if (breaking == true) kill_children(size, pids);

		printf("[parent] dead child: %u\n", dead_pid);
		int idx = -1;
		for (unsigned int _ = 0; _ < size; _++) {
			if (pids[_] != dead_pid) continue;
			idx = _;
			break;
		}
		printf("[parent] mark fd %d to zero.\n", fds[idx]);
		fds[idx] = 0;
	}
	return 1;
}

int main(int argc, char** argv)
{

	for (int _ = 1; _ < argc; _++) {
		if (!strcmp("-B", argv[_])) {
			breaking = 0;
		}
	}

	char cmd1[] = "while true; do date; sleep 2; done";
	/* char cmd2[] = "while true; do date +%s; sleep 3; done"; */
	char cmd2[] = "echo 1";

	char* programs[2];

	programs[0] = cmd1;
	programs[1] = cmd2;

	char* prefix[PROG_LENGTH];
	int l = 0;
	for (int _ = 0; _ < PROG_LENGTH; _++) {
		int c = _ % 5;
		char _prefix[128] = {0};
		char num[10] = {0};
		sprintf(num, "%d", _ + 1);
		strncat(_prefix, colors[c], strlen(colors[c]));
		strncat(_prefix, " worker", 7);
		strncat(_prefix, num, strlen(trim(num)));
		strncat(_prefix, " | ", 3);
		strncat(_prefix, ANSI_COLOR_RESET, strlen(ANSI_COLOR_RESET));
		l = strlen(trim(_prefix));
		prefix[_] = calloc(1, l);
		strncat(prefix[_], trim(_prefix), l);
		printf("prefix: %s\n", _prefix);
	}

	int fds[PROG_LENGTH];
	int pids[PROG_LENGTH];

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

	// select_ioloop(pids, fds, prefix);
	epoll_ioloop(pids, fds, prefix);

}

void select_ioloop(int pids[], int fds[], char * prefix[])
{

	for (int i = 0;i < PROG_LENGTH; i++) {
		printf("prefix %d: %s\n", i, prefix[i]);
	}

	for (;;) {

		reap_children(progs, pids, fds);

		fd_set readfds;
		FD_ZERO(&readfds);
		int max_fd = 0;

		for(int _ = 0; _ < PROG_LENGTH; _++) {
			if (fds[_] > 0) {
				printf("[parent] fd %d still alive\n", fds[_]);
				FD_SET(fds[_], &readfds);
			}
			else {
				printf("[parent] daed fd\n");
			}
			if (fds[_] > max_fd) max_fd = fds[_];
		}

		printf("[parent] about to select\n");
		int rc = select(
			max_fd + 1,
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

void epoll_ioloop(int pids[], int fds[], char * prefix[])
{
	int epfd = epoll_create(EPOLL_QUEUE_LEN);
	int res = 0;

	printf("fd0: %d\n", fds[0]);
	printf("fd1: %d\n", fds[1]);

	struct epoll_event ev1;
	ev1.events = EPOLLIN | EPOLLPRI | EPOLLERR | EPOLLHUP;
	ev1.data.fd = fds[0];
	res = epoll_ctl(epfd, EPOLL_CTL_ADD, fds[0], &ev1);

	struct epoll_event ev2;
	ev2.events = EPOLLIN | EPOLLPRI | EPOLLERR | EPOLLHUP;
	ev2.data.fd = fds[1];
	res = epoll_ctl(epfd, EPOLL_CTL_ADD, fds[1], &ev2);

	struct epoll_event * events = calloc(
		MAXEVENTS, sizeof(struct epoll_event));

	for (;;) {

		sleep(5);
		int n = epoll_wait(epfd, events, 10, 10000);
		printf(">>>>> n: %d\n", n);
		for (int i = 0; i < n; i++) {

			printf("fd: %d\n", events[i].data.fd);
			printf("ERR: %d\n", events[i].events & EPOLLERR);
			printf("HUP: %d\n", events[i].events & EPOLLHUP);
			printf("IN: %d\n", events[i].events & EPOLLIN);
			printf("PRI: %d\n", events[i].events & EPOLLPRI);

			if (events[i].events & EPOLLERR) {
				fprintf(stderr, "epoll error\n");
				close(events[i].data.fd);
			}
			else if (events[i].events & EPOLLHUP) {
				reap_children(progs, pids, fds);
				epoll_ctl(
					epfd, EPOLL_CTL_DEL,
					events[i].data.fd, NULL);
				// sleep(1);
				continue;
			}
			else if (events[i].data.fd == fds[0] ||
					 events[i].data.fd == fds[1]) {

				for(int _ = 0; _ < PROG_LENGTH; _++) {
					if (events[i].data.fd == fds[_]) {
						printf("[parent] ready index: %d, fd: %d\n",
							   _,
							   fds[_]);
						read_output(fds[_], prefix[_]);
						printf("[parent] read complete\n");
					}
				}

			}
			else {
				fprintf(stderr, "impossible?\n");
			}
		}
	}

	free(events);
}
