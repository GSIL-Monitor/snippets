#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>


#define BACKLOG_SIZE 10
#define BUFSIZE 100
#define SOCKPATH "unix.sock"

static int sock;

void signal_handler(int sig) {
	if (sig == SIGINT || sig == SIGTERM) {
		close(sock);
		if (unlink(SOCKPATH) == -1) {
			perror("cannot remove socket");
		}
		exit(0);
	}
}

void * socket_server () {
	// create socket fd
	sock = socket(AF_INET, SOCK_DGRAM, 0);

	if (sock == -1) {
		perror("socket error");
		exit(-1);
	}

	/*
	if (fcntl(sock, F_SETFL, O_NONBLOCK) == -1) {
		perror("fcntl error");
		exit(-1);
	}
	*/

	// create address
	struct sockaddr_un addr;
	memset(&addr, 0, sizeof(addr));
	addr.sun_family = AF_INET;
	strncpy(addr.sun_path, SOCKPATH, sizeof(addr.sun_path)-1);

	// bind socket to address
	if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
		perror("bind error");
		exit(-1);
	}

	if (listen(sock, BACKLOG_SIZE) == -1) {
		perror("listen error");
		exit(-1);
	}

	char * buf = calloc(sizeof(char), BUFSIZE);

	int rc = 0;
	int client = 0;
	while (1) {
		memset(buf, 0, BUFSIZE);
		client = accept(sock, NULL, NULL);
		if (client == -1) {
			// strerror(errno);
			perror("accept error");
			continue;
		}
		rc = read(client, buf, BUFSIZE);
		if (rc == -1) {
			perror("read error");
			exit(-1);
		}
		else if (rc == 0) {
			printf("client EOF\n");
			close(client);
		}
		else if (rc > 0) {
			write(client, buf, strlen(buf) + 1);
			printf("got %u bytes: %s\n", rc, buf);
		}
	}
	pthread_exit(NULL);
}

int main()
{

	signal(SIGINT, signal_handler);
	signal(SIGTERM, signal_handler);

	pthread_t p;
	pthread_create(&p, NULL, socket_server, NULL);

	srand(20);
	int r;

	while (1) {
		sleep(1);
		r = rand();
		printf("main loop, %d\n", r);
	}

	// void ** p_exit = NULL;
 	// pthread_join(p, p_exit);

	return 0;
}
