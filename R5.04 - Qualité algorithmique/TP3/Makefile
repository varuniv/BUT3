prog: valgrind.o
	gcc -o prog valgrind.o

valgrind.o: valgrind.c
	gcc -c valgrind.c -g

log_vg: prog
	valgrind --tool=memcheck --leak-check=full --log-file=$@ ./$< || true

.PHONY: clean
clean:
	rm -f prog valgrind.o log_vg