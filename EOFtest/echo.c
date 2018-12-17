#include <netdb.h>
#include <sys/socket.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

#define EHCO_PORT    6666
#define MAX_CLIENT_NUM        10

int main()
{
    int socketfd;
    socketfd = socket(AF_INET, SOCK_STREAM, 0);

    if(socketfd == -1)
    {
        printf("errno=%d ", errno);
        exit(1);
    }
    else
    {
        printf("socket create successfully ");
    }

    int reuse=1;
    if (setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR,(const char*)&reuse,sizeof(int)) == -1)
    {
        printf("setsockopt SO_REUSEADDR FAILED! ERROR[%d] ERRORINFO[%s]\n", errno, strerror(errno));
        exit(1);
    }

    struct sockaddr_in sa;
    bzero(&sa, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_port = htons(EHCO_PORT);
    sa.sin_addr.s_addr = htons(INADDR_ANY);
    bzero(&(sa.sin_zero), 8);

    if(bind(socketfd, (struct sockaddr *)&sa, sizeof(sa))!= 0)
    {
        printf("bind failed ");
        printf("errno=%d ", errno);
        exit(1);
    }
    else
    {
        printf("bind successfully ");
    }

    //listen
    if(listen(socketfd ,MAX_CLIENT_NUM) != 0)
    {
        printf("listen error ");
        exit(1);
    }
    else
    {
        printf("listen successfully ");
    }

    int clientfd;
    struct sockaddr_in clientAdd;
    char buff[101];
    // char content[] ="1\t77895\t3\n2\t44678\t3\n3\t22456\t1\n4\t24562\t1\n5\t34764\t65\n";
    char content[] = "/usr/local/tmp/tmp";

    socklen_t len = sizeof(clientAdd);
    int closing = 0;
    while( closing == 0  && (clientfd = accept(socketfd, (struct sockaddr *)&clientAdd, &len)) >0 )
    {
        int n;
        while((n = recv(clientfd,buff, 100,0 )) > 0)
        {
			printf("%d",n);
        
		}
		int length = strlen(content);
		send(clientfd, content, length, 0);
        close(clientfd);
    }

    close(socketfd);

    return 0;
}
