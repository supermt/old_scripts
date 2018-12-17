# Python Web 服务器详细设计

<!-- TOC -->

- [Python Web 服务器详细设计](#python-web-服务器详细设计)
  - [GUI 设计](#gui-设计)
    - [功能组件](#功能组件)
    - [相关逻辑](#相关逻辑)
  - [响应线程设计](#响应线程设计)
    - [功能设计](#功能设计)

<!-- /TOC -->

## GUI 设计

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

## 响应线程设计

### 功能设计

- 接受 HTTP 请求报文
  - 在这里，我们使用的是传入参数的方式
- 解析 HTTP 请求报文
  - 按行分割（该部分内容来自定义）
  - 按分隔符切分各行
    - 首部行，或称资源行
    - 请求头部行
    - 空行
    - 请求体，不分割
- 解析请求资源，来源是首部行
  - 请求方法
  - 请求资源
  - HTTP 协议版本号
- 按照各个资源的请求方式，switch(request_method)，分配各个响应逻辑
  - get_handler
  - post_handler
  - delete_handler
  - default_handler
- 根据响应情况，封装响应报文
  - 响应头
    - 一部分根据响应情况填充
      - content_type
      - content_length
    - 一部分与响应情况无关
      - Server
      - date
  - 响应体
    - 默认返回情况
    - 错误返回情况
    - 实体返回情况
- socket 传送