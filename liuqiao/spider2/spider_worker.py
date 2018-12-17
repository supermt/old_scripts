#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from urllib.parse import quote
import socket
import os
import math
import urllib.request
from bs4 import BeautifulSoup
import time
import sqlite3
import datetime
import spider_queue

TABLENAME="PAPER"

def get_article_count(keywordval):
  print(keywordval)
  index_url='http://search.cnki.com.cn/Search.aspx?q='+quote(keywordval)+'&rank=&cluster=&val=&p='#quote方法把汉字转换为encodeuri?
  html = urllib.request.urlopen(index_url).read()
  soup = BeautifulSoup(html, 'html.parser')
  maxpage = 1
  try:
    pagesum_text = soup.find('span', class_='page-sum').get_text()
    maxpage = math.ceil(int(pagesum_text[7:-1]) / 15)
  except AttributeError:
    pass
  
  return maxpage,index_url

def get_paper_urls(page_url,page_count):
  result = []
  for page in range(0,page_count):
    current_page = page_url+str(page*15)
    html = urllib.request.urlopen(current_page).read()
    soup = BeautifulSoup(html,'html.parser')

    all = soup.find_all('div', class_='wz_content')

    for string in all:
        item = string.find('a', target='_blank')#文章标题与链接
        href = item.get('href')# 获取文章url
        result.append(href)
  return result
    

def get_author_unit(soup):
  authorUnitScope = soup.find('div', style='text-align:left;', class_='xx_font')
  author_unit = ''
  author_unit_text = authorUnitScope.get_text()
  auindex = author_unit_text.find('：', 0)+1
      
  for k in range(auindex, len(author_unit_text)):
    if author_unit_text[k] == '\n' or author_unit_text[k] == '\t' or author_unit_text[k] == '\r' or author_unit_text[k] == '】' or author_unit_text[k] == ';':
        continue
    if author_unit_text[k] == ' ':
        continue
    if author_unit_text[k] != '【':
        author_unit = author_unit + author_unit_text[k]
    if author_unit_text[k] == '【' and k != auindex:
        break
  return author_unit


def paper_worker(paper_url):
  html = urllib.request.urlopen(paper_url).read()
  soup = BeautifulSoup(html, 'html.parser')

  title_scope = soup.find_all('div', style="text-align:center; width:740px; font-size: 28px;color: #0000a0; font-weight:bold; font-family:'宋体';")
  abstract_scope = soup.find_all('div', style='text-align:left;word-break:break-all')
  author_text = soup.find_all('div', style='text-align:center; width:740px; height:30px;')

  title_text=''

  for title in title_scope:
    title_text+=title.get_text()


  abstract_text=''

  for abstract in abstract_scope:
    abstract_text+=abstract.get_text()

  authors=[]
  author_unit=''
  try:
    author_unit = get_author_unit(soup)
  except AttributeError:
    pass

  for item in author_text:
    authors+=(item.get_text().split())

  spider_queue.queue_operator.add_records(authors)

  for i in range(len(authors)):
    authors[i] = authors[i] + "@" + author_unit
  
  
  return {"title":title_text,"abstract":abstract_text,"authors":authors}

def record_to_sql(paper):
  return "INSERT INTO "+TABLENAME+" (url,title,abstract,authors) \
          VALUES (\'"+ paper["url"]+"\',\'"+ paper["title"]+"\',\'"+paper["abstract"]+"\',\""+str(paper["authors"])+"\")"

def insert_into_sqlite(connect,sqls):
  cursor = connect.cursor()
  for sql in sqls:
    cursor.execute(sql)
  connect.commit()

def worker_thread(db_name,keywordval):
    connect = sqlite3.connect(db_name)
    connect.execute("DROP TABLE IF EXISTS "+TABLENAME+";")

    table_struct = '''(ID INTEGER PRIMARY KEY AUTOINCREMENT,
       url           VARCHAR(255)    NOT NULL,
       title            VARCHAR(100)     NOT NULL,
       authors            VARCHAR(200)     NOT NULL,
       abstract        TEXT);'''
    create_sql = "CREATE TABLE " + TABLENAME + table_struct
    connect.execute(create_sql)
    connect.commit()
    c = connect.cursor()

    #构造不同条件的关键词搜索
    values = {
           '全文': 'qw',
           '主题': 'theme',
           '篇名': 'title',
           '作者': 'author',
           '摘要':'abstract'
    }
    
    page_count,index_url = (get_article_count(keywordval))

    urls = get_paper_urls(index_url,page_count)
    results = []
    for url in urls:
      result = paper_worker(url)
      result['url']=url  
      results.append(result)
    sqls = []
    for result in results:
      sqls.append(record_to_sql(result))
    # print(sqls)
    insert_into_sqlite(connect,sqls)
    # print(len(sqls))

if __name__ == '__main__':
  start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  cf = ConfigParser()
  cf.read("Config.conf", encoding='utf-8')
  keyword = cf.get('base', 'keyword')# 关键词
  searchlocation = cf.get('base', 'searchlocation') #搜索位置
  keywordval = str(searchlocation)+':'+str(keyword)
  spider_queue.queue_operator.reboot(keyword)
  worker_thread(start,keywordval)