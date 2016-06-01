#include <string.h>
#include <curl/curl.h>
#include <json-c/json.h>



int main(int argc, char ** argv)
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

	CURL *curl;
	CURLcode res;

	curl = curl_easy_init();

	if (curl == NULL) {
		return 1;
	}

	curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:4567/post-json");
	curl_easy_setopt(curl, CURLOPT_POST, 1L);
	curl_easy_setopt(curl, CURLOPT_POSTFIELDS, b);
	// curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, strlen(b));
	curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

	struct curl_slist *chunk = NULL;
	chunk = curl_slist_append(chunk, "Content-Type: application/json");
	res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);

	res = curl_easy_perform(curl);

	if (res != CURLE_OK) {
		fprintf(
			stderr,
			"curl_easy_perform() failed: %s\n",
			curl_easy_strerror(res));
	}

	curl_easy_cleanup(curl);

	curl_slist_free_all(chunk);
	json_object_put(jobj);
	return 0;
}
