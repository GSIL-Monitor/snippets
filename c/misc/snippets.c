#include <stdio.h>
#include <string.h>
#include <time.h>


int time_delta(int delta, char * p) {
	if (delta <= 0) {
		return 1;
	}

	if (delta == 1) {
		snprintf(p, 13, "   1 second");
		return 0;
	}

	if (delta < 60) {
		snprintf(p, 13, "%4d seconds", delta);
		return 0;
	}

	if (delta == 60) {
		snprintf(p, 13, "   1 minute");
		return 0;
	}

	if (delta < 3600) {
		snprintf(p, 13, "%4d minutes", delta / 60);
		return 0;
	}

	if (delta == 3600) {
		snprintf(p, 13, "   1 hour");
		return 0;
	}

	if (delta < 86400) {
		snprintf(p, 13, "%4d hours", delta / 3600);
		return 0;
	}

	if (delta == 86400) {
		snprintf(p, 13, "   1 day");
		return 0;
	}

	if (delta <= 604800) {
		snprintf(p, 13, "%4d days", delta / 86400);
		return 0;
	}

	if (delta > 604800) {
		snprintf(p, 13, "%4d weeks", delta / 604800);
		return 0;
	}

	return 1;
}


int main(int argc, char** argv)
{
	char buf[20] = {'\0'};

	time_delta(0, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(1, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(59, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(60, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(3599, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(3600, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(86399, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(86400, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(604799, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	time_delta(1464620011, buf);
	printf("%s\n", buf);
	memset(buf, 20, 0);

	return 0;
}
