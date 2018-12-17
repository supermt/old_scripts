#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sched
import spider_worker
import threading
from threading import Timer
import datetime
import spider_cleaner
from configparser import ConfigParser
import spider_queue

LIMIT = 2
thread_count = 0
lock = threading.Lock()


def loop_thread(keywordval):
  global thread_count
  start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  db_name = "knowledge_graph"
  db_name = db_name+str(start)+keywordval+".db"
  threading.Thread(target=spider_worker.worker_thread,args=(db_name,keywordval,)).start()
  spider_cleaner.main(db_name,0)
  lock.acquire()
  try:
    thread_count-=1
  finally:
    lock.release()

def loop_starter(keyword,searchlocation):
  search_origin =  str(searchlocation)+':'+str(keyword)
  origin_thread = threading.Thread(target=loop_thread,args=(search_origin,))
  origin_thread.start()
  origin_thread.join()

  global thread_count
  while (1):
    current_name = spider_queue.queue_operator.get_record()
    if current_name != None and thread_count <= LIMIT:
      current_name = current_name.decode('utf-8')
      new_thread = threading.Thread(target=loop_thread,args=(str(searchlocation)+":"+str(current_name),))
      new_thread.start()
      new_thread.join()
      lock.acquire()
      try:
        thread_count+=1
      finally:
        lock.release()
    else:
      pass

if __name__ == '__main__':
  cf = ConfigParser()
  cf.read("Config.conf", encoding='utf-8')
  keyword = cf.get('base', 'keyword')# 关键词
  searchlocation = cf.get('base', 'searchlocation') #搜索位置
  spider_queue.queue_operator.reboot(keyword)
  loop_starter(keyword,searchlocation)