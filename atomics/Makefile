TARGET =	pg
OBJS =		main.o

CC =		gcc
CFLAGS =	-Wall -D_GNU_SOURCE
LDFLAGS =	-pthread

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $(TARGET)

%.o: %.c
	$(CC) $(CFLAGS) $< -c -o $@

sync1:
	gcc -Wall -D_GNU_SOURCE -lpthread -O0 main_sync.c
cpp:
	~/gcc-4.6-bin/bin/g++ -std='c++0x' -lpthread -fpermissive main_sync.c

clean:
	rm -f $(TARGET)
	rm -f $(OBJS)

call: clean all
