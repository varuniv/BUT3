# on précise le compilateur à utiliser
CC=gcc

# on précise la liste des fichiers objets
OBJ=main.o liste.o

# on précise les options de compilation
CFLAGS=-std=c11 -Wall -Wextra -pedantic -ggdb

main: $(OBJ)
	$(CC) $(CFLAGS) $^ -o $@
# Règle patron pour la génération des fichiers objet.
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

log_vg: main
	valgrind --tool=memcheck --leak-check=full --log-file=$@ ./$< || true

.PHONY : clean
clean:
	rm -f main *.o