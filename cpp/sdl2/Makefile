include config.mk

SRC = $(wildcard snippets.cxx)
OBJ = $(SRC:.cxx=.o)

all: options snippets

options:
	@echo snippets build options
	@echo "CFLAGS = ${CFLAGS}"
	@echo "LDLAGS = ${LDFLAGS}"
	@echo "CC = ${CC}"

config.h:
	cp config.def.h config.h

%.o : %.cxx
	${CC} -c ${CFLAGS} -o $@ $<

${OBJ}: config.h config.mk

snippets: ${OBJ}
	${CC} -o $@ ${OBJ} ${LDFLAGS}

clean:
	@echo cleaning
	rm -f snippets ${OBJ}

.PHONY: all options clean
