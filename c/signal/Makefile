include config.mk

SRC = $(wildcard snippets.c util/*.c)
OBJ = $(SRC:.c=.o)

all: options snippets

options:
	@echo snippets build options
	@echo "CFLAGS = ${CFLAGS}"
	@echo "LDLAGS = ${LDFLAGS}"
	@echo "CC = ${CC}"

config.h:
	cp config.def.h config.h

%.o : %.c
	@echo CC -o $@
	@${CC} -c ${CFLAGS} -o $@ $<

${OBJ}: config.h config.mk

snippets: ${OBJ}
	@echo CC -o snippets
	@${CC} -o $@ ${OBJ} ${LDFLAGS}

clean:
	@echo cleaning
	@rm -f snippets ${OBJ}

.PHONY: all options clean
