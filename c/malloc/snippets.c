#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define STEP 268435456

int main(int argc, char ** argv)
{

	if (argc <= 1) {
		printf("usage: %s <memory in bytes>\n", argv[0]);
		return 1;
	}
	unsigned long long desired = 0;
	unsigned long long assigned = 0;

	sscanf(argv[1], "%llu", &desired);

	printf("desired: %llu\n", desired);

	unsigned long long cnt = desired / STEP;

	for (unsigned int i = 0; i < cnt; i++) {
		printf("allocating %u / %llu\n", i, cnt);
		char * s = calloc(sizeof(char), STEP);
		if (s == NULL) {
			perror("error when allocating memory..");
			break;
		}
		memset(s, 0, STEP);
		assigned += STEP;
	}

	printf("done allocating memory, exit...\n");

	return 0;
}
