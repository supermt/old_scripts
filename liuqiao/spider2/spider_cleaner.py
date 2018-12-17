#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sched
import spider_worker
from threading import Timer
import datetime
import sqlite3
import os

TABLENAME="PAPER"
GAPTIME = 5

def read_records(db_name , offset):
  record_count = 0
  connect = sqlite3.connect(db_name)
  c = connect.cursor()
  try:
    records = c.execute("SELECT id, url, title, authors, abstract  FROM " + TABLENAME + " LIMIT 100 OFFSET " + str(offset))
    
    for record in records:
      print(record)
      record_count+=1
  except sqlite3.OperationalError:
    pass

  return record_count

def remove_db(db_name):
  if os.path.exists(db_name):
    os.remove(db_name)

def main(db_name,offset):
  read_record = read_records(db_name,offset)
  if read_record != 0:  
    Timer(GAPTIME, main,(db_name,offset + read_record)).start()
  else:
    # all records read
    remove_db(db_name)
    

if __name__ == '__main__':
  main("knowledge_graph2018-06-10 02/24/07作者/余景寰.db",0)
  