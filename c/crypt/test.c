#define _XOPEN_SOURCE
#include <stdio.h>
#include <unistd.h>

int main()
{

  const char *password = "password";
  const char *salt = "";

  const char *rv = crypt(password, salt);

  printf("rv: %s\n", rv);

  return 0;
}
