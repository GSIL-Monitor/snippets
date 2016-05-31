#include <pwd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#include "util/util.h"



int main(int argc, const char** argv)
{

	if (argc == 1) {
		fprintf(stderr, "%s <username>\n", argv[0]);
		exit(-1);
	}

	const char * username = argv[1];

	printf("attempting to setuid to %s\n", username);

	uid_t uid = getuid();
	printf("uid is: %u\n", uid);

	gid_t gid = getgid();
	printf("gid is: %u\n", gid);

	struct passwd *p;

	if ((p = getpwnam(username)) == NULL) {
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

	printf("home: %s\n", p->pw_dir);
	printf("size: %lu\n", strlen(p->pw_dir));

	char stdout[1024] = {'\0'};
	char stderr[1024] = {'\0'};
	const char *env[4] = {'\0'};
	char _home[strlen(p->pw_dir) + 6];
	char _user[strlen(username) + 6];
	char _login[strlen(username) + 7];
	snprintf(_home, strlen(p->pw_dir) + 6, "%s%s", "HOME=", p->pw_dir);
	snprintf(_user, strlen(username) + 6, "%s%s", "USER=", username);
	snprintf(_login, strlen(username) + 7, "%s%s", "LOGIN=", username);
	env[0] = _home;
	env[1] = _user;
	env[2] = _login;
	env[3] = NULL;

	int status;

	char *command = "/bin/bash -i -l -c 'echo $SSH_AGENT_PID'";
	printf("%s\n", command);

	setgid(1000);
	setuid(1000);
	subprocess(
		command,
		env, &status,
		1024, stdout,
		1024, stderr);

	printf("stdout: %s\n", stdout);
	printf("stderr: %s\n", stderr);

	return 0;
}
