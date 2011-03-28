//Local.c
#include <jni.h>
#include "Local.h"
#include <stdio.h>

#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

void error(const char *msg)
{
    perror(msg);
    exit(0);
}

JNIEXPORT void JNICALL
Java_Local_send(JNIEnv *env, jobject obj, jstring hostname, jint port)
{
    int str_len;
    const char *host;
    str_len = (*env)->GetStringLength(env, hostname);    //get string length

    host = (*env)->GetStringUTFChars(env, hostname, 0); //get UTF-8 encoding char array
    
    int sockfd, portno, n;
    portno = port;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[256];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    // set the hostname
    server = gethostbyname(host);
    (*env)->ReleaseStringUTFChars(env, hostname, host);    //after using jstring object you must release it  
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);

    // set the port number
    serv_addr.sin_port = htons(portno);
    printf("Connecting...\n");
    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR connecting");
    printf("Please enter the message:");
    bzero(buffer,256);
    fgets(buffer,255,stdin);
    n = write(sockfd,buffer,strlen(buffer));
    if (n < 0) 
         error("ERROR writing to socket");
    bzero(buffer,256);
    n = read(sockfd,buffer,255);
    if (n < 0) 
         error("ERROR reading from socket");
    printf("%s\n",buffer);
    close(sockfd);

    return;
}
