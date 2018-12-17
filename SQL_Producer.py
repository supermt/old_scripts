#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random
import time
import sys


def randomFromValueArea(array):
    return array[random.randint(0,len(array)-1)]

if len(sys.argv) != 4:
  print "Missing Arguments , provide like ./SQL_Producer.py [RESULT_COUNT] [CONDITION_COUNT] [LOOP_TIME]"
else:

  RESULT_COUNT = int(sys.argv[1])
  CONDITION_COUNT = int(sys.argv[2])
  LOOP_TIME = int(sys.argv[3])

  table_description = "logtime:timestamp, svr_ip:string, user_ip:string, port:long, host:string, url:string, req_args:string, strrange:string, http_code:long, send_bytes:long, handle_time:long, refer:string, user_agent:string, stdform:string, uin:long, isnormalclosed:long, url302:string, cdn:long, sample:long, filesize:long, inner_errcode:long, inner_filename:string, bizid:long, flow:long, clientappid:string, reverse_proxy:string, oc_id:string, str_reserve:string, vkey:string, int_reserve:long, province:long, isp:long, log_type:long, get_store_time:long, deliver_time:long, store_type:long, bit_rate:long, media_time:long, media_type:string, req_type:long, inner_errmsg:string, content_type:string, store_ip:string, resolution:long, reserve1:long, reserve2:long, reserve3:long, reserve4:string, reserve5:string"

  time_format = "%Y-%m-%d %H:%M:%S"

  column_list = table_description.split(", ")
  index_area = range(len(column_list)-1)

  operator_list = ["==","!=",">","<","<=",">="]

  value_area_sets = []

  value_area_array= []

  result_columns = []

  source_file = open('sourcefile', 'r')

  loglist = source_file.readlines()
  for i in range(0,len(column_list)):
    value_area_sets.append(set())

  for logline in loglist:
    column_in_row = logline.split('\t')
    # print column_in_row
    for i in range(0,len(column_in_row)):
      value_area_sets[i].add(column_in_row[i])

  for i in range(0,49):
    value_area_array.append([])
    for value in value_area_sets[i]:
      value_area_array[i].append(value)

  for loop in range(0,LOOP_TIME):
    # produce result columns
    target_column_count = RESULT_COUNT
    sample_columns = random.sample(index_area,target_column_count)

    for index in sample_columns:
      result_columns.append(column_list[index].split(":")[0])

    #produce conditions

    predicate_list = []

    target_column_count = CONDITION_COUNT

    sample_columns = random.sample(index_area,target_column_count)

    for index in sample_columns:
      # print column_list[index]
      atom_predicate= column_list[index].split(":")[0]
      
      if column_list[index].split(":")[1] == "long" :
        # case long
        condition = operator_list[random.randint(0,5)]
        atom_predicate += " "+condition+" "
        atom_predicate += randomFromValueArea(value_area_array[index])
      elif column_list[index].split(":")[1] == "string" :
        #case string
        condition = operator_list[random.randint(0,1)]
        atom_predicate += " "+condition+" \""
        atom_predicate += randomFromValueArea(value_area_array[index])
        atom_predicate += "\""
      else:
        #case timestamp
        condition = operator_list[random.randint(0,5)]
        atom_predicate += " "+condition+" \""
        atom_predicate += randomFromValueArea(value_area_array[index])
        atom_predicate += "\""

      predicate_list.append(atom_predicate)


    SQL = "SELECT "

    for i in range(0,len(result_columns)-1):
      SQL += result_columns[i]+","
    SQL += result_columns[len(result_columns)-1]

    SQL+=" WHERE "

    for i in range(0,len(predicate_list)-1):
      SQL += predicate_list[i]
      if random.randint(0,1) == 1:
        SQL += " AND "
      else:
        SQL += " OR "
    SQL += predicate_list[len(predicate_list)-1]

    print SQL + "\n"
