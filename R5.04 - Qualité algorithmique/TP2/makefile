all: main
CFLAGS+= -Wall -Wextra -Wconversion -g -O0

main: main.o liste_chainee.o 
	gcc -o main main.o liste_chainee.o 

%.o: %.c liste.h
	gcc -c $(CFLAGS) $<