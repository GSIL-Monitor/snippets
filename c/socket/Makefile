include config.mk

SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

all: options unix-server unix-client

options:
	@echo build options:
	@echo "CFLAGS = ${CFLAGS}"
	@echo "LDFLAGS = ${LDFLAGS}"
	@echo "CC = ${CC}"

.o : %.c
	$(CC) -c $(CFLAGS) -o $@ $<

clean:
	rm -f unix-server ${OBJ}

unix-server: unix-server.o
	$(CC) $(LDFLAGS) -o unix-server unix-server.o

unix-client: unix-client.o
	$(CC) $(LDFLAGS) -o unix-client unix-client.o
