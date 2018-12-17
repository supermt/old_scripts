import numpy as np
import matplotlib.pyplot as plt
import time
import socket,struct

def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


target_file = open('targetpack', 'r')
loglist = target_file.readlines()
# used to recognize how many columns these lines would have
# longestline = 0
# for logline in loglist:
#   logline = logline.split('\t')
#   if len(logline) > longestline:
#     longestline = len(logline)
# print longestline //every line has only 49 columns

num_columns = 49

# columns with none sense
escape_columns = [4,5,6,21,28,29,27,40]

column_table = []

for i in range(0,num_columns):
  column_table.append([])

for j in range(0,20):
  logline = loglist[j]
# for logline in loglist:
  logline = logline.split('\t')
  for i in range(0,num_columns):
    if i == 0:
      target_unit = time.mktime(time.strptime(logline[0], "%Y-%m-%d %H:%M:%S"))
    # elif i in escape_columns:
    #   target_unit = ""
    else:
      target_unit = logline[i]
    column_table[i].append(target_unit)

rows = len(column_table[0])

# timestamp column

# x = range(0,rows)
# y = column_table[0]

# server_ip column
# y=[]
# for singleIP in column_table[2]:
#   y.append(ip2long(singleIP))

# y = np.unique(y)
# x = range(0,len(y))
# serverIPs = []
# for singleIP in y:
#   serverIPs.append((y))
# print serverIPs

# client IP column
# y=[]
# for singleIP in column_table[2]:
#   y.append(ip2long(singleIP))

# print "Unique Client IP length : "+str(len(y)) +"\t rows count : "+str(rows)

# port / does this column really means anything?

# y=[]
# for singlePort in column_table[3]:
#   y.append(int(singlePort))

# plt.hist(y)

# plt.show()

# y = np.unique(y)

# print "Unique Server Port length : "+str(len(y)) +"\t rows count : "+str(rows)

# server host names
# hosts = {"":0}
# for i in range(0,len(column_table[4])):
#   if hosts.get(str(column_table[4][i]),0) == 0:
#     hosts[str(column_table[4][i])]=1
#   else:
#     hosts[str(column_table[4][i])]+=1

# for host_tuple in hosts:
#   print host_tuple + "\t" + str(hosts.get(host_tuple))

# video name
hosts = {"":0}
for i in range(0,len(column_table[5])):
  if hosts.get(str(column_table[5][i]),0) == 0:
    hosts[str(column_table[5][i])]=1
  else:
    hosts[str(column_table[5][i])]+=1

for host_tuple in hosts:
  print host_tuple + "\t" + str(hosts.get(host_tuple))

for i in range(0,49):
  print str(i)+"\t"+str(column_table[i][0])