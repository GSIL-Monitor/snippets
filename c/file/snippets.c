#include <libgen.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>



int main(int argc, const char ** argv)
{
	// const char path[] = "/root";
	const char path[] = "/tmp";

	int p = access(path, W_OK);

	printf("%d\n", p);
	return 0;
}
