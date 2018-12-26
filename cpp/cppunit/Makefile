CC = gcc
CFLAGS =
LDFLAGS = -lcppunit
SRC = $(wildcard *.cc)
OBJ = ${SRC:.cc=.o}

all: options test

options:
	@echo "CFLAGS = ${CFLAGS}"
	@echo "LDLAGS = ${LDFLAGS}"
	@echo "CC = ${CC}"
	@echo "OBJ = ${OBJ}"

%.o: %.cc
	g++ -c ${CFLAGS} -o $@ $<

test: ${OBJ}
	g++ -o $@ ${OBJ} ${LDFLAGS}

clean:
	echo ${OBJ}
	rm -f *.o
