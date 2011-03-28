all:
	javac Local.java
	javah -jni Local
	gcc -fPIC Local.c -c -I/opt/sun-jdk-1.5.0.22/include -I/opt/sun-jdk-1.5.0.22/include/linux
	gcc Local.o -shared -o libcore.so 
	
