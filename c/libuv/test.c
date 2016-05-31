#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <uv.h>


struct timer_data_t {
	int seconds;
};
typedef struct timer_data_t timer_data_t;

uv_loop_t *loop;

void test(uv_timer_t *handle)
{
        timer_data_t *data = handle->data;
	printf("sleeping for %d seconds\n", data->seconds);
	sleep(data->seconds);
	printf("executing test.\n");
}


int main(int argc, char **argv)
{

	loop = uv_default_loop();

	uv_timer_t timer1;
	timer_data_t *data1 = malloc(sizeof(timer_data_t));
	data1->seconds = 3;
	timer1.data = data1;

	uv_timer_init(loop, &timer1);
	uv_timer_start(&timer1, (uv_timer_cb) &test, 0, 1000);

	uv_timer_t timer2;
	timer_data_t *data2 = malloc(sizeof(timer_data_t));
	data2->seconds = 0;
	timer2.data = data2;

	uv_timer_init(loop, &timer2);

	uv_timer_start(&timer2, (uv_timer_cb) &test, 0, 1000);
	uv_timer_start(&timer1, (uv_timer_cb) &test, 0, 1000);


	return uv_run(loop, UV_RUN_DEFAULT);
}
