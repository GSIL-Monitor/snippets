#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char** argv)
{
	if (argc == 1) {
		return -1;
	}

	char* params[argc - 1];
	size_t size = 0;

	for (int _ = 0; _ < argc - 1; _++) {
		params[_] = argv[_ + 1];
		printf("%s ", params[_]);
		size += strlen(params[_]) + 1;
	}
	printf("\n");
	char command[size];
	memset(command, 0, sizeof(command));

	for (int _ = 0; _ < argc - 1; _++) {
		strncat(command, params[_], strlen(params[_]));
		strncat(command, " ", 1);
	}

	printf("%s\n", command);

	execl("/bin/bash", "bash", "-c", params, (char *) 0);
	perror("exec error");
	return 0;
}
