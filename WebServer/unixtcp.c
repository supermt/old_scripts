#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

#define SERV_PORT   10086
#define MAX_LINE    1024


int main(int argc, char **argv)
{
    int listenfd, connfd;
    pid_t    childpid;
    socklen_t    cli_len;
    struct sockaddr_in    cliaddr,servaddr;
    
    cli_len = sizeof(cliaddr);
    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if(listenfd < 0)
    {
        printf("create socket error!\n");
        exit(1);
    }
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(SERV_PORT);
    if(bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
    {
        printf("bind error!\n");
        exit(1);
    }
    listen(listenfd, 5);
    puts("listening");
    connfd = accept(listenfd, (struct sockaddr*)&cliaddr, &cli_len);
    char buf[MAX_LINE]="";
    read(connfd, buf, MAX_LINE);
    puts(buf);
    char *a=strtok(buf," ");
    a=strtok(NULL," ");
    char filename[200]={"/Users/MT"};
    strcat(filename,a);
    puts(filename);
    FILE * openfile=fopen(filename,"rb");
    char resp[200];
    char content[MAX_LINE]="";
    int length=0;
    if (!openfile){
        puts("404");
        sprintf(resp,"HTTP/1.1 404 Not Found\r\nServer:233\r\nContent-Type: text/html\r\n\r\n<BODY><P>The server could not fulfill\r\n<P><BODY>");
        //char resp[200] = "HTTP/1.1 404 Not Found\r\nServer:233\r\nContent-Length: 0\r\nContent-Type: text/html\r\n\r\n";
    }
    else{
        length=fread(content,1,MAX_LINE,openfile);
    }
    //char resp[200] = "HTTP/1.1 200 OK\r\nServer:233\r\nContent-Length: ";
    sprintf(resp,"HTTP/1.1 200 OK\r\nServer:233\r\nContent-Length: %d\r\nContent-Type: text/html\r\nContent-Type: text/html\r\n\r\n%s",length,content);
    //strcat();
    puts("OK");
    //"\r\nContent-Type: text/html\r\n\r\n";
    //获取数据流
    //str_echo(connfd);
    send(connfd,resp,sizeof(resp),0);
    close(connfd);/*parent close connected socket*/
    puts("OK");
    return 0;
}