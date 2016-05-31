#include <stdio.h>
#include <yaml.h>
#include <unistd.h>



struct statd_config_t {
  char *host;
  int port;
};


struct monitor_item_t {
	int interval;
	char *name;
	char *command;
};

struct monitor {
	struct monitor_item_t* item;
	struct monitor* next;
};


struct statd_config_t*
read_statsd_config(yaml_parser_t *parser, yaml_token_t *token)
{
	printf("processing stats config.\n");

	struct statd_config_t *config = malloc(sizeof(struct statd_config_t));

	int level = 0;

	/* state=1: key, state=0: other */
	int state = 0;
	char* key;

	do {

		/* usleep(100000); */
		yaml_parser_scan(parser, token);

		/* printf("token.type: %d\n", token->type); */
		/* printf("level: %d\n", level); */

		switch (token->type) {

		case YAML_BLOCK_MAPPING_START_TOKEN: level++; break;
		case YAML_BLOCK_END_TOKEN: level--; break;
		case YAML_KEY_TOKEN: level++; state = 1; break;
		case YAML_VALUE_TOKEN: level++; state = 0; break;

	  case YAML_SCALAR_TOKEN: ;
			level--;

			yaml_char_t *value = token->data.scalar.value;

			/* printf("got: %s\n", value); */

			if (state == 1) {
				/* key */
				key = (char *) value;
			}
			else if (state == 0) {
				/* value */
				if (strcmp(key, "host") == 0) {
					config->host = (char *) value;
				}
				else if (strcmp(key, "port") == 0) {
					int port;
					sscanf((char *)value, "%d", &port);
					config->port = port;
				}

			}

			// TODO: error handling
			break;

		default: ;
			// printf("got token.type: %d\n", token->type);
		}
	} while (level > 0);

	// read through
	yaml_parser_scan(parser, token);

	return config;
}

struct monitor*
read_monitor_config(yaml_parser_t *parser, yaml_token_t *token)
{
	struct monitor* head = NULL;
	struct monitor* prev = NULL;
	struct monitor* current = NULL;

	int level = 0;
	/* state=1: key, state=0: other */
	int state = 0;
	char* key;

	do {

		yaml_parser_scan(parser, token);

		switch (token->type) {
		case YAML_STREAM_END_TOKEN: break;
			/* token types */
		case YAML_KEY_TOKEN: state = 1; break;
		case YAML_VALUE_TOKEN: state = 0; break;
			/* block delimeters */
		case YAML_BLOCK_SEQUENCE_START_TOKEN: level++; break;
		case YAML_BLOCK_ENTRY_TOKEN:
			/* start new sequence item ( which means a new item ) */
			if (prev == NULL) {
				/* first one, is head*/
				current = malloc(sizeof(struct monitor));
				current->item = malloc(sizeof(struct monitor_item_t));
				current->next = NULL;
				head = current;
			}
			if (prev != NULL) {
				current = malloc(sizeof(struct monitor));
				current->item = malloc(sizeof(struct monitor_item_t));
				current->next = NULL;
				prev->next = current;
			}
			prev = current;
			break;
		case YAML_BLOCK_END_TOKEN: level--; break;
		case YAML_BLOCK_MAPPING_START_TOKEN: level++; break;
		case YAML_SCALAR_TOKEN: ;

			yaml_char_t* value = token->data.scalar.value;

			if (state == 1) {
				// key
				key = (char *) value;
				// printf("key: %s\n", key);
			}
			else if (state == 0) {
				// value
				if (strcmp(key, "interval") == 0) {
					int in;
					sscanf((char *)value, "%d", &in);
					current->item->interval = in;
				}
				else if (strcmp(key, "name") == 0) {
					current->item->name = (char *) value;
				}
				else if (strcmp(key, "command") == 0) {
					current->item->command = (char *) value;
				}
			}

		default: ;
			// printf("Got token of type %d\n", token->type);
		}

	} while (level > 0);

	return head;
}


int main()
{

	yaml_parser_t *parser = malloc(sizeof(yaml_parser_t));
	if(!yaml_parser_initialize(parser)) {
		fputs("Failed to initialize parser!\n", stderr);
	}

	FILE *fh = fopen("config.yml", "r");
	if (fh == NULL) {
		fputs("Failed to open file 'config.yml'", stderr);
	}

	yaml_parser_set_input_file(parser, fh);


	yaml_token_t token;

	/* state=1: reading value | nonthing, state=0: reading key */
	int state = 0;

	do {

		yaml_parser_scan(parser, &token);

		// printf("%d\n", token.type);

		switch (token.type) {

		case YAML_KEY_TOKEN: state = 0; break;
		case YAML_VALUE_TOKEN: state = 1; break;
		case YAML_SCALAR_TOKEN: ;
			yaml_char_t *value = token.data.scalar.value;

			if (state == 0) {
				char* key = (char *) value;

				if (strcmp(key, "statd") == 0) {

					// read through the value token
					yaml_parser_scan(parser, &token);

					struct statd_config_t *config =
						read_statsd_config(parser, &token);

					printf("statd host: %s\n", config->host);
					printf("statd port: %d\n", config->port);

				}

				if (strcmp(key, "monitor") == 0) {

					// read through the value token
					yaml_parser_scan(parser, &token);

					struct monitor *monitor =
						read_monitor_config(parser, &token);

					if (monitor == NULL) {
						fputs("no monitor items detected!\n", stderr);
					}

				}

			}
			break;

		default: ;
			//printf("Got token of type %d\n", token.type);
		}

	} while (token.type != YAML_STREAM_END_TOKEN);

	yaml_parser_delete(parser);
	fclose(fh);
	printf("done.\n");
	return 0;
}
