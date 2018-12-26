#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>
#include <errno.h>

#define BUFSIZE 100
#define SOCKPATH "unix.sock"

int main()
{
	// create socket
	int sock = socket(AF_UNIX, SOCK_STREAM, 0);

	// create address
	struct sockaddr_un addr;
	memset(&addr, 0, sizeof(addr));
	addr.sun_family = AF_UNIX;
	strncpy(addr.sun_path, SOCKPATH, sizeof(addr.sun_path)-1);

	if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
		perror("connect error");
		exit(-1);
	}

	if (fcntl(sock, F_SETFL, O_NONBLOCK) == -1) {
		perror("fcntl error");
		exit(-1);
	}

	char msg[] = "hello";

	if (write(sock, msg, strlen(msg) + 1) == -1) {
		perror("write error");
		exit(-01);
	}

	char * buf = calloc(sizeof(char), BUFSIZE);
	int rc = 0;
	while (1) {
		rc = read(sock, buf, BUFSIZE);
		if (rc == -1) {
			if (errno == EAGAIN) {
				break;
			}
			perror("read error");
			exit(-1);
		}
		else if (rc == 0) {
			// read end
			break;
		}
		else {
			printf("got response %u bytes: %s\n", rc, buf);
		}
	}

	close(sock);

	return 0;
}
