#include <stdio.h>
#include <string.h>
#include <time.h>

int main(int argc, char** argv)
{

	char buf[20] = {'\0'};
	time_t now = time(NULL);

	strftime(buf, 20 , "%Y-%m-%d %H:%M:%S", localtime(&now));
	printf("%s\n", buf);
	memset(buf, 0, sizeof(buf));
	strftime(buf, 9, "%H:%M:%S", localtime(&now));
	printf("%s\n", buf);

	return 0;
}
