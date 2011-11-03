namespace android {
namespace renderscript {

    class Context {
    public:
        Context();
        static struct Props {
            bool mLogTimes;
            bool mLogScripts;
            bool mLogObjects;
            bool mLogShaders;
            bool mLogShadersAttr;
            bool mLogShadersUniforms;
            bool mLogVisual;
            bool mRemoteClient;
            bool mRemoteServer;
            int mRemoteIP;
        } props;

        void printSomething();
    };
};};
