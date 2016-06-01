#include <stdio.h>
#include <stdlib.h>
#include "iniparser/src/iniparser.h"

int parse_init_file(char * ini_name)
{
	dictionary * ini = iniparser_load(ini_name);
	iniparser_dump(ini, stderr);

	const char * host =
		iniparser_getstring(ini, "database.zhuanqian:host", NULL);
	printf("host: %s\n", host);

	const int port =
		iniparser_getint(ini, "database.zhuanqian:port", 0);
	printf("port: %d\n", port);

	iniparser_freedict(ini);
	return 0;
}

int main(int argc, char ** argv)
{
	if (argc < 2) {
		printf("%s <file>\n", argv[0]);
		exit(1);
	}
	parse_init_file(argv[1]);

	return 0;
}
