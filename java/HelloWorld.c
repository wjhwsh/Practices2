//HelloWorld.c
#include <jni.h>
#include "HelloWorld.h"
#include <stdio.h>

JNIEXPORT void JNICALL
Java_HelloWorld_helloworld(JNIEnv *env, jobject obj, jstring param)
{
    int str_len;
    char *buf;
    str_len = (*env)->GetStringLength(env, param);    //get string length

    buf = (*env)->GetStringUTFChars(env, param, 0); //get UTF-8 encoding char array
    printf("UTF param:%s[length:%d]\n",buf,str_len);
    (*env)->ReleaseStringUTFChars(env, param, buf);    //after using jstring object you must release it  

    buf = (*env)->GetStringChars(env, param, 0);       //get unicode encoding char array
    printf("Char param:%s[length:%d]\n",buf,str_len);
    (*env)->ReleaseStringChars(env, param, buf);      //release string

    printf("Message: %s\n", buf);
    return;
}
