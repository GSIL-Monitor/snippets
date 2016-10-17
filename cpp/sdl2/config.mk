# version
VERSION = 0.0.1

LIBS = -lSDL2 -lpthread

# flags
CFLAGS := -g -std=c++11 -Wpedantic -Wall -D_XOPEN_SOURCE=600 -DVERSION=\"${VERSION}\"
LDFLAGS := -g ${LIBS}
CC = g++
