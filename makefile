CC=clang 
CFLAGS=-c -Wall -pedantic -std=c99
LIBS=-lm # note: the l means library, m means math
SWIG=swig
#export LD_LIBRARY_PATH=`pwd`
#python3.11 TestFiles/A2Test1.py
#python3.11 TestFiles/A2Test2.py --> make svg files
#python3.11 server.py 52174
#localhost:52174/shoot.html
#ps -fA | grep python
#kill -9 1163891

all: a4

a4: libphylib.so _phylib.so

libphylib.so: phylib.o
	$(CC) phylib.o -shared -lm -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c 
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/Library/Frameworks/Python.framework/Versions/3.11/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	$(CC) phylib_wrap.o -shared -L. -L/Library/Frameworks/Python.framework/Versions/3.11/lib/ -lpython3.11 -lphylib -o _phylib.so

clean:
	rm -f *.o *.so a4 phylib_wrap.c phylib.py
	