#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

int daemon(const char * logfile)
{
	pid_t pid = 0;
	pid_t sid = 0;
	int log_fd = 0;

	log_fd = open(logfile, O_WRONLY | O_CREAT | O_APPEND, 0644);

	if (log_fd < 0){
		fprintf(stderr, "daemon open() failed: %s", strerror(errno));
		exit(1);
	}

	pid = fork();
	if (pid < 0) {
		close(log_fd);
		fprintf(stderr, "daemon fork() failed: %s", strerror(errno));
		exit(1);
	}

	if (pid > 0) {
		// parent
		close(log_fd);
		exit(0);
	}

	umask(0);

	sid = setsid();
	if (sid < 0) {
		fprintf(stderr, "daemon setsid() failed: %s", strerror(errno));
		exit(1);
	}

	chdir("/");

	close(0);
	close(1);
	close(2);

	dup2(log_fd, 1);
	dup2(log_fd, 2);
	close(log_fd);

	return 0;
}


int main(int argc, char** argv)
{
	daemon("log.txt");

	while (1) {
		char buf[20] = {'\0'};
		time_t now = time(NULL);

		strftime(buf, 20 , "%Y-%m-%d %H:%M:%S", localtime(&now));
		printf("%s\n", buf);
		fflush(stdout);
		sleep(1);
	}

	return 0;
}
