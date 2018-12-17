#-*- coding:utf-8 -*-

import datetime
import os
import Configuration
from LogProducer import LOGGER
from sys import argv

# 定义一系列常量
NEXT_LINE = "\r\n"
# 正常返回的首部行
RESPONSE_HEADER_OK = "HTTP/1.1 200 OK"
MSG_OK = "Oh! It's really OK"
# 错误的请求
RESPONSE_HEADER_BAD_REQUEST = "HTTP/1.1 400 BAD REQUEST"
MSG_BAD_REQUEST = "Method Can Not Be Processed"
MSG_POST_CANNOT_CREATE = "The File is already exists, we cannot process"

# 服务器内部错误
RESPONSE_HEADER_BAD_GATEWAY = "HTTP/1.1 502 BAD GATEWAY"
MSG_BAD_GATEWAY = "Sorry , the Server is Broken"
# 无法找到文件
RESPONSE_HEADER_NOT_FOUND = "HTTP/1.1 404 NOT FOUND"
MSG_NOT_FOUND = "There is no such file"

# 行名 Connection
LINE_CONNECTION = "Connection"
DEFAULT_CONNECTION = "close"

# 行名 Date
LINE_DATE = "Date"
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

# 行名 Server
LINE_SERVER = "Server"
SERVER_NAME = "ZRJ 2016220303034"

# 行名 Content-Type
LINE_TYPE = "Content-Type"

# 行名 Content-Length
LINE_LENGTH = "Content-Length"

# 行间 分隔符
SYMBOL_SPLIT =": "

argc = len(argv)
Configuration.init(Configuration.parse_system_arg(argv).get("-p", None))
BASE_DIR = Configuration.BASE_DIR
type_dict = Configuration.type_dict

def httpRequestHandler(connection, HTTPRequest):#传递参数
  line_list = HTTPRequest.split("\r\n")
  resource_header = line_list.pop(0).split(' ') #将第一行（资源行、首部行、请求行）按照空格分割为请求方法、请求资源和 http 版本
  if len(line_list) != 0:
    # 获取请求体
    request_body = line_list.pop(len(line_list)-1)
    # 去除空行
    line_list.pop(len(line_list)-1)

  request_headers = {}#初始化一个字典（用于存储请求头代表的键值对）

  for line in line_list:
    entry = line.split(SYMBOL_SPLIT) # 按照 ': ' 分割为键值对
    if len(entry) == 2:
      request_headers[entry[0]] = entry[1]
  
  # 处理 Connection/返回日期/服务器信息三个首部行
  response_header = process_response_header(request_headers)#响应头返回结果存入字典

  response_body,response_status_header = process_resource(
                      resource_header[0],
                      resource_header[1],
                      resource_header[2],
                      request_body,
                      response_header)#根据请求资源构建响应报文的头部，处理资源的同时添加 Content-Type 和 Content-Length（其他的已经在process_response_header处理完成）

  LOGGER.info("Request for : %s using %s method returns in %s",resource_header[1],resource_header[0],response_status_header)
  # 添加首部行
  http_response = response_status_header + NEXT_LINE

  # 遍历添加响应头
  for (key,value) in response_header.items():
    http_response = http_response + key + SYMBOL_SPLIT + str(value) + NEXT_LINE #迭代添加响应头部行

  # 添加空行，之后的内容都是响应体
  http_response = http_response + NEXT_LINE
  http_response = http_response + response_body

  send_response(connection,http_response)


def process_response_header(request_headers):#（）内为传入的参数
  response_header = {}#等同于 创建一个新的对象，如 Java 中的 New

  # 设置连接信息
  if request_headers.has_key(LINE_CONNECTION):
    value = request_headers.get(LINE_CONNECTION)
    response_header[LINE_CONNECTION] = value
  else:
    response_header[LINE_CONNECTION] = DEFAULT_CONNECTION
  # 设置返回日期
  response_header[LINE_DATE] = datetime.datetime.utcnow().strftime(DATE_FORMAT)#代表当前时间的字符串
  # 设置服务器信息
  response_header[LINE_SERVER] = SERVER_NAME
  # 返回该字典以备后用
  return response_header
  
def process_resource(request_method, request_resource, HTTPVersion, request_body,response_header):
  request_method = request_method.upper()
  try:
    if request_method == "GET":
      return processGET(request_resource, response_header)
    elif request_method == "POST":
      return processPOST(request_resource, request_body, response_header)
    elif request_method == "DELETE":
      return processDELETE(request_resource, response_header)
    else:
      response_header[LINE_LENGTH] = len(MSG_BAD_REQUEST)
      return MSG_BAD_REQUEST, RESPONSE_HEADER_BAD_REQUEST
  except Exception, e:
    LOGGER.error(str(e))
    return MSG_BAD_GATEWAY, RESPONSE_HEADER_BAD_GATEWAY
  

def processGET(request_resource, response_header): #request_resource为请求的资源（请求方法后），是一个相对路径
  if request_resource[len(request_resource) - 1] == "/":#最后一个字符是‘/’ 代表当前资源为一个文件夹
    request_resource = request_resource + "index.html"#在访问文件夹时转为访问该文件夹下的index.html文件
  LOGGER.debug("requesting" + request_resource)
  file_path = BASE_DIR + request_resource #绝对路径=基础路径（一般为当前路径）+相对路径
  if os.path.exists(file_path): #用 exists 函数判断 file_path 所指代的文件是否存在
    file_length = os.path.getsize(file_path)#python 如何获取文件大小
    response_header[LINE_TYPE] = type_dict.get("."+request_resource.split(".")[1]) #文件名.文件类型再加点才能查表，得到的结果为该文件在 HTTP 报文中的响应类型，将其设置到 Content-Type 首部行中
    target_file = open(file_path, "rb")#以二进制读取的形式打开该文件，将动作返回结果存入target_file中，target_file是 File 类的一个实例，其中提供了操作一个文件所需的各种方法
    response_body = target_file.read(file_length)#读的数据长度正好为文件本身的长度，即读取文件全部内容
    response_header[LINE_LENGTH] = str(file_length) #同132行
    return response_body, RESPONSE_HEADER_OK
  else:
    # 文件不存在，返回404
    return MSG_NOT_FOUND, RESPONSE_HEADER_NOT_FOUND

def processPOST(request_resource, request_body, response_header):
  file_path = BASE_DIR + request_resource #绝对路径=基础路径（一般为当前路径）+相对路径
  if os.path.exists(file_path): #用 exists 函数判断 file_path 所指代的文件是否存在
    response_header[LINE_LENGTH] = str(len(MSG_POST_CANNOT_CREATE))
    return MSG_POST_CANNOT_CREATE, RESPONSE_HEADER_BAD_REQUEST
  else:
    target_file = open(file_path, "wb")
    try:
      response_body = target_file.write(request_body)
      target_file.flush()#那该写的完全写入（保存）
      target_file.close()#关闭该文件
      return MSG_OK, RESPONSE_HEADER_OK
    except:
      return MSG_BAD_GATEWAY, RESPONSE_HEADER_BAD_GATEWAY

def processDELETE(request_resource, response_header):
  file_path = BASE_DIR + request_resource #绝对路径=基础路径（一般为当前路径）+相对路径
  if os.path.exists(file_path): #用 exists 函数判断 file_path 所指代的文件是否存在
    #删除
    try:
      os.remove(file_path)
      return MSG_OK, RESPONSE_HEADER_OK
    except:
      return MSG_BAD_GATEWAY, RESPONSE_HEADER_BAD_GATEWAY
  else:
    return MSG_NOT_FOUND, RESPONSE_HEADER_NOT_FOUND


def send_response(client_connection, http_response):
  # 一个标准的响应报文应该包含
    # 首部行
      # 状态行
      # 是否使用长连接，这个根据 Http 请求而定，Connection: keep-alive
      # 返回报文长度，Content-length，这里使用文件大小
      # 响应报文类型，Content-Type，根据文件类型进行查表操作
      # 返回日期，取当前时间戳，格式为 Wed, 11 Apr 2018 19:02:49 GMT
      # 服务器信息，Sever，这个地方可以附上个人信息防止抄袭行为
    # 一个空行
    # 报文内容，其可能的内容有
      # 简单报错信息：根据触发内容进行报错
      # 二进制数据流：无论是文字内容的文件还是多媒体文件，都可以以这种形式进行阅读和发送，这样的好处在于，可以避免多次数据转换带来的编码错误
      # 内容响应：针对 PUT、POST、DELETE 等资源操作类请求的回复，用简单语句描述

  client_connection.sendall(http_response) #要求代理人讲所有的信息发送给客户端
  client_connection.close() #关闭



