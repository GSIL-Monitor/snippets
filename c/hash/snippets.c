#include "string.h"
#include "stdio.h"
#include "uthash.h"

struct config_t {
	char name[255];
	UT_hash_handle hh;
};



int main(int argc, char** argv)
{

	struct config_t * configs = NULL;
	struct config_t * myconfig = calloc(sizeof(struct config_t), 1);
	sprintf(myconfig->name, "%s", "hello");

	HASH_ADD_STR(configs, name, myconfig);

	char * key = "hello";

	struct config_t * result = NULL;

	HASH_FIND_STR(configs, key, result);

	if (result == NULL) {
		printf("not found\n");
	}
	else {
		printf("found\n");
	}

	HASH_DEL(configs, result);

	HASH_FIND_STR(configs, key, result);

	if (result == NULL) {
		printf("not found\n");
	}
	else {
		printf("found\n");
	}

}
