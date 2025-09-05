# on précise le compilateur à utiliser
CC=gcc

# on précise la liste des fichiers objets
OBJ=tp1_main.o tp1_exos.o

# on précise les options de compilation
CFLAGS=-std=c11 -Wall -Wextra -pedantic -ggdb

main: $(OBJ)
	$(CC) $(CFLAGS) $ˆ -o $@

# Règle patron pour la génération des fichiers objet.
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
.PHONY: clean
clean:
	rm -f main *.o