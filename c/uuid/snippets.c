#include <stdio.h>
#include <string.h>
#include <time.h>
#include <uuid/uuid.h>

int main(int argc, char** argv)
{

	char buf[20] = {'\0'};
	time_t now = time(NULL);

	strftime(buf, 20 , "%Y-%m-%d %H:%M:%S", localtime(&now));
	printf("%s\n", buf);
	memset(buf, 0, sizeof(buf));
	strftime(buf, 9, "%H:%M:%S", localtime(&now));
	printf("%s\n", buf);

	uuid_t uu;
	uuid_clear(uu);
	uuid_generate(uu);
	char b[36] = {'\0'};
	uuid_unparse_upper(uu, b);
	printf("uuid: %s\n", b);
	uuid_clear(uu);

	return 0;
}
