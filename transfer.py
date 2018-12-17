#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time

def long2byte(parameter_list):
  byteNum = byte[8]
  for ix in range(0,8) :
      offset = 64 - (ix + 1) * 8
      byteNum[ix] = (byte) ((num >> offset) & 0xff)

  return byteNum

source_file = open('sourcefile', 'r')
loglist = source_file.readlines()
num_columns = 49
escape_columns = [4,5,6,21,28,29,27,40]

column_table = []

for i in range(0,num_columns):
  column_table.append([])

for logline in loglist:
  logline = logline.split('\t')
  for i in range(0,num_columns):
    if i == 0:
      target_unit = long(time.mktime(time.strptime(logline[0], "%Y-%m-%d %H:%M:%S")))
    # elif i in escape_columns:
    #   target_unit = ""
    else:
      target_unit = logline[i]
    column_table[i].append(target_unit)
    print i,target_unit