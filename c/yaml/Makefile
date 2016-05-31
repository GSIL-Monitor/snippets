CC :=gcc
CFLAGS :=-I. -ggdb
LIBS :=-lyaml
LDFLAGS := -g


.PHONY: all

clean:
	$(RM) *.o test

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)


test: test.o
	$(CC) -O0 -ggdb -o test test.o $(LIBS)

all: test
