CC := gcc
CFLAGS := -I. $(shell mysql_config --cflags)
LIBS := $(shell mysql_config --libs)

all: version

version.o:
	$(CC) -Wa,--verbose -v -c -o version.o $(CFLAGS) version.c

version: version.o
	$(CC) -Wall -Wl,--verbose -o version $(LIBS) version.o

clean:
	rm -f *.o version
