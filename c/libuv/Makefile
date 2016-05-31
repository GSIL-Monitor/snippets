CC :=gcc
CFLAGS := -Wall -ggdb
LIBS :=-luv
LDFLAGS := -ggdb


all: test

clean:
	$(RM) *.o test

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)


test: test.o
	$(CC) -ggdb -o test test.o $(LIBS)
