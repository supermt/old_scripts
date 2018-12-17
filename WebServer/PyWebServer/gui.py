#!/usr/bin/env python
#-*- coding:utf-8 -*-

from Tkinter import *  
import os
import Configuration
import time
import thread
import subprocess

start_command = "./WebServer.py -d=True"
shut_command = "./WebServer.py -c=True"
open_conf_command = "open ./conf"

class App:  
    def __init__(self, master):  
        Configuration.init() # 初始化配置内容

        self.btn_frame = Frame(master)  
        self.btn_frame.pack(side=BOTTOM)

        self.start_button_text=StringVar()
        self.start_button_switch=0
        self.start_button_text.set("Start The Server")
        self.start_button = Button(self.btn_frame, textvariable=self.start_button_text,command=self.start_daemon_server)  
        self.start_button.pack(side=LEFT) #此处side为LEFT表示将其放置 到frame剩余空间的最左方  
        self.conf_button = Button(self.btn_frame, text="Open Config Directory", command=self.open_conf_directory)  
        self.conf_button.pack(side=LEFT)
        self.shut_button = Button(self.btn_frame, text="Shut Down The Application", command=self.shut_down)  
        self.shut_button.pack(side=LEFT)

        # 设置 log_frame 用于显示日志
        
        self.log_frame = Frame(master)
        self.log_frame.pack(side=LEFT)
        self.log_box = Text(self.log_frame, height=20, width=80)
        S = Scrollbar(self.log_frame)
        S.pack(side=RIGHT, fill=Y)
        self.log_box.pack(side=LEFT, fill=Y)
        S.config(command=self.log_box.yview)
        self.log_box.config(yscrollcommand=S.set)
        self.log_box.insert(END,"GUI System is online")

        # 设置 status_frame 用于显示系统状态
        self.status_frame = Frame(master)
        self.status_frame.pack(side=RIGHT)
        self.status_text_var=StringVar()
        self.status_text_var.set("Server is Not Running")
        self.label = Label(self.status_frame,textvariable=self.status_text_var)
        self.label.pack()

    def start_daemon_server(self):  
        self.start_button_switch = self.start_button_switch+1
        if self.start_button_switch % 2:
          # 开启服务器
          # 直接调用 WebServer 中的函数会造成阻塞，选择使用系统命令运行
          os.system(start_command)
          server_info = "Server is Running on\n port:"+str(Configuration.PORT)+" \n base directory:\n"+Configuration.BASE_DIR
          self.status_text_var.set(server_info)
          self.start_button_text.set("Stop The Server")
          self.log_box.insert(END,"\nWeb Server Online")
        else:
          # 关闭服务器
          os.system(shut_command)
          self.status_text_var.set("Server is Not Running")
          self.start_button_text.set("Start The Server")
          self.log_box.insert(END,"\nWeb Server Offline")


    def open_conf_directory(self):
      os.system(open_conf_command)
      self.log_box.insert(END,"\nOpening Configuration Directory")

    def shut_down(self):
      os.system(shut_command)
      self.btn_frame.quit()

def read_log(log_box,logfile):
  # 调用系统命令 tail ，使用-f 参数，以追加的形式进行监听
  command='tail -f '+logfile
  # 使用 Linux 下的 Pipe 机制，读取目标指令的输出内容
  popen=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
  while True:
    # 每次出现新行后将其追加在系统之后
    line=popen.stdout.readline().strip()
    log_box.insert(END,"\n"+line)

os.system(shut_command)
win = Tk()
app = App(win)
logfile='./log/default.log'
thread.start_new_thread(read_log,(app.log_box,logfile))
win.mainloop()