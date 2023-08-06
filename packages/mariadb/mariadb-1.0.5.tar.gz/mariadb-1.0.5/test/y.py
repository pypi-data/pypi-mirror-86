import resource
import mariadb

# import mysql.connector as driver

from time import sleep
count=0
db = mariadb.connect()

def conf():
  return {"user" : "root", "port" : 13000, "host" : "127.0.0.1"}

begin= last_usage = resource.getrusage(resource.RUSAGE_SELF)
while count < 4000:

     pool= mariadb.ConnectionPool(pool_name="test_connection_pool_add")
     try:
         default_conf= conf()
         pool.set_config(**default_conf)
     except:
         pool.close()
         raise

     for i in range(1,6):
         pool.add_connection()

     pool.close()
     count+= 1

     last_usage = resource.getrusage(resource.RUSAGE_SELF)
     if last_usage[2] - begin[2] > 0:
       print("total mem diff %s" % (last_usage[2] - begin[2]))
     begin= last_usage
