#-*- coding:utf-8 -*-
import ConfigParser
import os

HOST = '127.0.0.1' #代指本机地址
PORT = 10086 #端口号

PWD = os.path.split(os.path.realpath(__file__))[0]

# 基础路径,设置为当前路径
BASE_DIR = PWD

# Content-Type 对照表
type_dict = {}

CONFIG_PATH = PWD + "/conf/"

MAIN_CONF_PATH = CONFIG_PATH + "log.config"

LOG_CONFIG_PATH = CONFIG_PATH + "main.config"

def init(config_path = None):
  if (config_path == None):
    # 没有参数
    setConfigPath()
  else:
    setConfigPath(config_path)

  global MAIN_CONF_PATH

  global LOG_CONFIG_PATH

  LOG_CONFIG_PATH = CONFIG_PATH + "log.config"

  MAIN_CONF_PATH = CONFIG_PATH + "main.config"

  # 读取配置文件，获取 Content-Type 中各文件对应返回值
  filename = CONFIG_PATH + 'Content-Type.csv'
  global type_dict
  type_table = open(filename,"r") 
  lines = type_table.read().splitlines()
  for line in lines: #lines(数组)中的每个元素（line）做如下操作     
      entry = line.split("\t")#entry（是一个键值对 key - value）用\t 分割子串 子串以字符串数组的形式组织也就是 entry
      type_dict[entry[0]] = entry[1]#设置键值 ResponseThread 模块名（封装单元）  type_dict变量名

  main_config = ConfigParser.RawConfigParser()
  main_config.read(MAIN_CONF_PATH)

  # 初始化服务器监听配置
  global HOST
  global PORT
  global BASE_DIR

  HOST = main_config.get("Host Basic","HOST")
  PORT = main_config.getint("Host Basic","PORT")
  BASE_DIR = main_config.get("Host Basic","BASE_PATH")

def setConfigPath(path = None):
  global CONFIG_PATH
  # 获取配置文件路径
  if path == None:
    # 未配置路径
    CONFIG_PATH = PWD + "/conf"
  elif path[0]=='/':
    # path 是绝对路径
    CONFIG_PATH = path
  else:
    # path 是相对路径
    CONFIG_PATH = PWD + '/' + path
  
  if (CONFIG_PATH[len(CONFIG_PATH)-1] != '/'):
    # 结尾不是 / ，统一处理
    CONFIG_PATH = CONFIG_PATH + "/"

  if (os.path.exists(CONFIG_PATH)):
    return CONFIG_PATH
  else:
    raise RuntimeError("CONFIG_PATH : " + CONFIG_PATH +" Invalid" )
  
def parse_system_arg(argv):
    argc = len(argv)
    start_args = {}
    accept_args = ["-d","-c","-p"]
    if argc == 1:
      return start_args
    else:
      for arg_index in range(1,argc): # argv[0] 是程序名，需要过滤掉
          if argv[arg_index].split("=")[0] in accept_args:
              start_args[argv[arg_index].split("=")[0]]=argv[arg_index].split("=")[1]
          else:
              sys.stderr.write("can not explain the arguments")
              exit(1)
      return start_args
