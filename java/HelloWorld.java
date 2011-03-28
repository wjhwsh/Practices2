//HelloWorld.java
class HelloWorld {
    public native void helloworld(String param);

    static {
        System.load("/home/modcarl/Practices/java/libhello.so");
    }

    public static void main(String[] args) {
        new HelloWorld().helloworld("HelloWorld");
    }
}
