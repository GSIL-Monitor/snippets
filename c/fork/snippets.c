#include <asm/errno.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>



int main(int argc, char** argv)
{
	int p_status = 0;
	int p = waitpid(0, &p_status, 0);

	printf("%d\n", p == -1);

	printf("%d\n", errno);
	printf("%d\n", errno == ECHILD);
	printf("%s\n", strerror(errno));

	return 0;
}
