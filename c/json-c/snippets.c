#include <stdio.h>
#include <string.h>
#include <json-c/json.h>

int main(int argc, char** argv)
{
	struct json_object* jobj;
	jobj = json_object_new_object();
	json_object_object_add(jobj, "status", json_object_new_string("ok"));
	struct json_object*	data_arr;
	data_arr = json_object_new_array();

	json_object_array_add(data_arr, json_object_new_int(1));
	json_object_array_add(data_arr, json_object_new_int(2));
	json_object_array_add(data_arr, json_object_new_int(3));
	json_object_object_add(jobj, "data", data_arr);
	json_object_object_add(jobj, "message", json_object_new_string(""));

	const char *b = json_object_to_json_string(jobj);
	printf("%s\n", b);
	json_object_put(jobj);

	return 0;
}
