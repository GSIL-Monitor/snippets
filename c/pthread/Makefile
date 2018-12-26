include config.mk

SRC = $(wildcard snippets.c util/*.c)
OBJ = $(SRC:.c=.o)

all: options snippets fork

options:
	@echo snippets build options
	@echo "CFLAGS = ${CFLAGS}"
	@echo "LDLAGS = ${LDFLAGS}"
	@echo "CC = ${CC}"

config.h:
	cp config.def.h config.h

%.o : %.c
	${CC} -c ${CFLAGS} -o $@ $<

${OBJ}: config.h config.mk

snippets: ${OBJ}
	${CC} -o $@ ${OBJ} ${LDFLAGS}

fork: fork.o
	${CC} -o $@ fork.o ${LDFLAGS}

clean:
	rm -f snippets ${OBJ}

.PHONY: all options clean
