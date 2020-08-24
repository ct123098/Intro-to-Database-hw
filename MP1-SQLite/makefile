
student: sqlite3.h sqlite3.c sqlite3.o student.cpp
	g++ student.cpp sqlite3.o -lpthread -ldl -o student --std=c++11 -O2

sqlite3.o: sqlite3.h sqlite3.c
	gcc -c sqlite3.c -lpthread -ldl -o sqlite3.o

clean:
	rm -f student sqlite3.o
