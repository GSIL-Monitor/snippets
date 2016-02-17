#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>


int main(int argc, char **argv)
{
	if (argc == 1) {
		fprintf(stderr, "%s <username>\n", argv[0]);
		exit(-1);
	}

	printf("attempting to setuid to %s\n", argv[1]);

	uid_t uid = getuid();
	printf("uid is: %u\n", uid);

	gid_t gid = getgid();
	printf("gid is: %u\n", gid);

	struct passwd *p;

	if ((p = getpwnam(argv[1])) == NULL) {
		perror("getpwnam() error\n");
	}

	printf("pw_name: %s\n", p->pw_name);
	printf("pw_uid: %d\n", p->pw_uid);
	printf("pw_gid: %d\n", p->pw_gid);
	printf("pw_dir: %s\n", p->pw_dir);
	printf("pw_shell: %s\n", p->pw_shell);

	if (uid != 0) {
		fprintf(stderr, "only root can change uid/gid.\n");
		exit(-1);
	}

	int g = setgid(p->pw_gid);
	if (g == -1) {
		perror("setgid() failed\n");
	}

	int u = setuid(p->pw_uid);
	if (u == -1) {
		perror("setuid() failed\n");
	}

	uid = getuid();
	printf("uid is: %u\n", uid);

	gid = getgid();
	printf("gid is: %u\n", gid);

	execl("/bin/bash", "bash", "-c", "id", (char *) 0);
	perror("exec error");

	return 0;
}
