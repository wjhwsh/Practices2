//ClientSide.java
class Local {
    public native void send(String hostname, int port);

    static {
        System.load("/home/modcarl/Practices/java/socket/version2/libcore.so");
    }

    public static void main(String[] args) {
        new Local().send("140.112.29.194", 2000);
    }
}
