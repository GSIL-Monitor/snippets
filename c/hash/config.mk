# version
VERSION = 0.0.1

LIBS = -lcrypto -lpthread

# flags
CFLAGS := -g -std=c99 -Wpedantic -Wall -Os -D_XOPEN_SOURCE=600 -DVERSION=\"${VERSION}\"
LDFLAGS := -g -static ${LIBS}
# CC = cc
