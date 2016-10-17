#include <netdb.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

int send_msg(const char*, const int, const char*);
void * metric_thread();
void * cleanup();

static int metric_running = 0;

void * cleanup() {
	metric_running = 0;
	return NULL;
}

void * metric_thread()
{
	pthread_cleanup_push(cleanup, NULL);
	char buf[10] = {'\0'};
	time_t now;

	while (1) {
		now = time(NULL);
		sprintf(buf, "%lu\n", (unsigned long) now);
		send_msg("127.0.0.1", 4000, buf);
		memset(buf, '\0', 10);
		sleep(1);
	}
	pthread_cleanup_pop(NULL);
	pthread_exit(NULL);
}

int send_msg(const char* host, const int port, const char* msg)
{
	int s = socket(AF_INET, SOCK_DGRAM, 0);

	if (s < 0) {
		perror("cannot create socket");
		return -1;
	}

	struct sockaddr_in myaddr;
	memset((char *)&myaddr, 0, sizeof(myaddr));
	myaddr.sin_family = AF_INET;
	myaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	myaddr.sin_port = htons(0);

	int b = bind(
		s,
		(struct sockaddr *)&myaddr,
		sizeof(myaddr));

	if (b < 0) {
		perror("bind failed");
		return 0;
	}

	struct sockaddr_in servaddr;
	struct hostent *hp;

	memset((char*)&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(port);

	hp = gethostbyname(host);
	if (!hp) {
		fprintf(stderr, "could not obtain address of %s\n", host);
		return -1;
	}

	memcpy((void *)&servaddr.sin_addr, hp->h_addr_list[0], hp->h_length);

	int f = sendto(
		s,
		msg,
		strlen(msg),
		0,
		(struct sockaddr *)&servaddr,
		sizeof(servaddr));

	if (f < 0) {
		perror("sendto failed");
		return -1;
	}

	close(s);
	return 0;
}

int main(int argc, char** argv)
{
	printf("my pid: %d\n", getpid());

	pthread_t p;
	void **p_exit = NULL;


	while(1) {
		if (metric_running == 0) {
			if (p) {
				pthread_join(p, p_exit);
			}
			pthread_create(&p, NULL, metric_thread, NULL);
			metric_running = 1;
		}
		sleep(1);
	}

	return 0;
}
