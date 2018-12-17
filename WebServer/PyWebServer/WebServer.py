#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import ResponseThread
import thread
import Configuration 
from LogProducer import *
from sys import argv
import sys, os

## Server Main Logic

def init_socket(HOST, PORT):#初始化一个接口

    # 以下四行基本是固定的，直接拷贝即可
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建一个 socket
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)# 为 listen_socket 这个类的实例设置固定属性
    listen_socket.bind((HOST, PORT)) # 将 listen_socket 这个 Socket 类实例绑定至 Host:PORT 端口
    listen_socket.listen(5) # 设置 listen_socket 的监听队列为 1，一般设置为5，具体区别可以上网查
    LOGGER.debug('Serving HTTP on port %s ...' % PORT) 
    print 'Serving HTTP on port %s ...' % PORT
    while True:
        client_connection, client_address = listen_socket.accept() # 返回两个变量 connection 为本次交流的全权代理 address 为连接发起者（即客户端）的地址
        HttpRequest = client_connection.recv(1024) # 接收最长为1024的请求内容，存储在 request 中
        LOGGER.debug(HttpRequest)
        # 创建新线程进入报文响应流程
        thread.start_new_thread(ResponseThread.httpRequestHandler,(client_connection,HttpRequest))
        
def start_web_server(path=None):
    Configuration.init(path)
    init_log(Configuration.LOG_CONFIG_PATH)
    init_socket(Configuration.HOST,Configuration.PORT) #调用上面那段函数

def daemonize (switch=0,stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    if switch == "True":
        #重定向标准文件描述符（默认情况下定向到/dev/null） 
        try:
            pid = os.fork()
        #父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。 
            if pid > 0: sys.exit(0) #父进程退出 
        except OSError, e:
            sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) ) 
            sys.exit(1)
        #从母体环境脱离 
        # os.chdir("/") chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。
        # 也可以改变到对于守护程序运行重要的文件所在目录 
        # 那么对于我们现在写的程序而言，最重要的文件夹实际上就是当前目录
        os.umask(0) #调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。 
        os.setsid() #setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。 

        #执行第二次fork 
        try:
            pid = os.fork()
            if pid > 0: sys.exit(0) # 第二个父进程退出
        except OSError, e:
            sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) ) 
            sys.exit(1)

        #进程已经是守护进程了，重定向标准文件描述符
        for f in sys.stdout, sys.stderr: f.flush() 
        si = open(stdin, 'r') 
        so = open(stdout, 'a+') 
        se = open(stderr, 'a+', 0) 
        os.dup2(si.fileno(), sys.stdin.fileno()) #dup2函数原子化关闭和复制文件描述符 
        os.dup2(so.fileno(), sys.stdout.fileno()) 
        os.dup2(se.fileno(), sys.stderr.fileno()) 
    else:
        pass

def shut_down(switch="False"):
    if switch == "True":
        command = "kill -9 `ps -ef|grep "+__file__+"|awk '{print $2}'`"
        os.system(command)

if __name__ == '__main__':# C语言中的 int main
    start_args = Configuration.parse_system_arg(argv)
    shut_down(start_args.get("-c","False"))
    daemonize(start_args.get("-d","False"),'/dev/null','log/daemon_stdout.log','log/daemon_error.log')                
    start_web_server(start_args.get("-p",None))