LIBS = -lpthread

CC := gcc
CFLAGS := -g -std=c99 -Wpedantic \
	-Wall -D_XOPEN_SOURCE=600
LDFLAGS := -g ${LIBS}
