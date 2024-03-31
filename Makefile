mathLib.so: mathLib.c
	gcc -shared -o mathLib.so -fPIC mathLib.c