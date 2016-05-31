#include <stdio.h>
#include <string.h>

int main()
{
	printf("%d\n", strcmp("1", "1"));
	printf("%d\n", strcmp("1", "12"));
	printf("%d\n", strcmp("1", "2"));

	return 0;
}
