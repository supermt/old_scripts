# Python Web 服务器详细设计

<!-- TOC -->

- [Python Web 服务器详细设计](#python-web-服务器详细设计)
  - [设计 GUI](#设计-gui)
    - [功能组件](#功能组件)
    - [相关逻辑](#相关逻辑)

<!-- /TOC -->

## 设计 GUI

### 功能组件

- 用文本框显示日志
- 用一个按钮来启动配置修改功能
- 用一个标签来监视 WebServer 的运行状态
- 用一个按钮来启动/关闭 WebServer 接口
- 用一个按钮来关闭程序

### 相关逻辑

- 组件绑定逻辑，即初始化过程
- start_daemon_server，启动 WebServer
- open_conf_directory，启动配置修改接口
- shut_down，关闭系统
- read_log，用于读取日志文件并追加在日志监听文本框内
