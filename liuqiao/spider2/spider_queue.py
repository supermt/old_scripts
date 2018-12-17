import redis

class Queue:

  def __init__(self,queue_name="knowledge_graph"):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    self.listname = queue_name
    self.operator = r

  def reboot(self,starter):
    self.operator.flushall()
    self.operator.set(starter,starter) 
  
  def add_records(self, dataset):
    for data in dataset:
      target = self.operator.get(data)
      if target == None:
        self.operator.set(data,data)    
        self.operator.rpush(self.listname,data)
  
  def get_record(self):
    record = self.operator.lpop(self.listname)
    return record


queue_operator = Queue()