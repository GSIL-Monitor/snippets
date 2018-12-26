#include <stdio.h>
#include <stdlib.h>

#include "ipipx.h"

int main(int argc, const char ** argv)
{

	ipipx_init("/home/momoka/Downloads/17monipdb.datx");

	char * result = calloc(1024, 1);

	ipipx_find("180.118.145.228", result);

	printf("result: %s\n", result);

	free(result);

	return 0;
}
