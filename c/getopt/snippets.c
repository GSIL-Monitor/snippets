#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>



int main(int argc, char** argv)
{
	extern char *optarg;
	extern int optind;

	int c, err = 0;
	int wflag = 0, bflag = 1;
	int interval = 0;
	int step = 0;
	int concurrency = 1;

	static char usage[] = "usage: %s [-w] [-i interval] "
		"[-s step] [-c concurrency] [-B] command... \n";

	while ((c = getopt(argc, argv, "wi:s:c:B")) != -1) {
		switch (c) {
		case 'w':
			wflag = 1;
			break;
		case 'i':
			sscanf(optarg, "%d", &interval);
			break;
		case 's':
			sscanf(optarg, "%d", &step);
			break;
		case 'c':
			sscanf(optarg, "%d", &concurrency);
			break;
		case 'B':
			bflag = 0;
			break;
		case '?':
			err = 1;
			break;
		}
	}

	if ((optind + 1) > argc) {
		/* need at least one argument */
		fprintf(stderr, "need at least one argument.\n");
		fprintf(stderr, usage, argv[0]);
		return -1;
	}
	else if (err) {
		fprintf(stderr, usage, argv[0]);
		return -1;
	}

	printf("warmup: %d\n", wflag);
	printf("breaking: %d\n", bflag);
	printf("interval: %d\n", interval);
	printf("concurrency: %d\n", concurrency);
	printf("step: %d\n", step);

	for (; optind < argc; optind++) {
		printf("argument: %s\n", argv[optind]);
	}

	return 0;
}
