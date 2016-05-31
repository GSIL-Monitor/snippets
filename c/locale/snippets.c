#include <locale.h>
#include <stdio.h>
#include <stdlib.h>


int main(int argc, const char ** argv)
{
	char default_lc_all[] = "en_US.utf8";
	char * lc_all = getenv("LC_ALL");
	if (lc_all == NULL) {
		printf("LC_ALL not set\n");
		lc_all = default_lc_all;
	}
	printf("LC_ALL: %s\n", lc_all);

	setlocale(LC_ALL, lc_all);

	return 0;
}
