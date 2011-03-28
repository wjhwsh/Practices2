all:
	javac HelloWorld.java
	javah -jni HelloWorld
	gcc -fPIC HelloWorld.c -c -I/opt/sun-jdk-1.5.0.22/include -I/opt/sun-jdk-1.5.0.22/include/linux
	gcc HelloWorld.o -shared -o libhello.so 
	
