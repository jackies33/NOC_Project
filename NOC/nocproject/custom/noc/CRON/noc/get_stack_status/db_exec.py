

import psycopg2
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import re
import clickhouse_driver
from pytz import timezone
from my_pass import pass_noc,user_noc

class PSQL_CONN():

                """
                Class for psql connection and collecting some data
                """

                def __init__(self,id1=None,list1=None):
                        self.id1=id1
                        self.list1 = list1
                        self.conn = psycopg2.connect(
                            host="10.50.50.170",
                            database="noc",
                            user=user_noc,
                            password=pass_noc,
                            sslmode='disable',
                        )
                        self.cur = self.conn.cursor()


                def postgre_conn_inv(self,*args):
                        self.cur.execute(f"select id,name,address,object_profile_id,bi_id,vendor from sa_managedobject where object_profile_id IN ({self.id1});")
                        tuple = (self.cur.fetchall())
                        return tuple

                def get_id(self, *args):
                        self.cur.execute(f"select id from sa_managedobjectprofile where name IN ({self.list1});")
                        tuple = (self.cur.fetchall())
                        return tuple


class MONGO():

      """class for connection and recieve data from mongo DB"""

      def __init__(self,id1=None,id2=None):
          self.id1=id1
          self.id2=id2



      def get_vendor(self,*args):
          name = ''
          client = MongoClient(f'mongodb://noc:{user_noc}@kr01-mongodb01:27017/{pass_noc}')
          db = client['noc']
          collection = db['noc.vendors']
          post_id = f"{self.id1}"
          find = collection.find_one({"_id" : ObjectId(post_id)})
          result={}
          if find:
              name = str(find.get("name"))
              id = str(find.get("_id"))
              id.split('ObjectId')
              result.update({"id":id,"name":name})
          return result

      def get_bi_id(self,*args):
          name = ''
          client = MongoClient(f'mongodb://noc:{user_noc}@kr01-mongodb01:27017/{pass_noc}')
          db = client['noc']
          collection = db['ds_managedobject']
          id = int(self.id2)
          find = collection.find({"_id" : id})
          #for d in find:
           #  print(d)



class CH():

    """Class for connection and execute command to CH server"""

    def __init__(self,mylist):
        self.mylist = mylist
        self.connection1 = clickhouse_driver.connect(
            host='10.50.50.177',
            port=9000,
            user=user_noc,
            password=pass_noc,
            database='noc'
        )
        self.connection2 = clickhouse_driver.connect(
            host='10.50.50.174',
            port=9000,
            user=user_noc,
            password=pass_noc,
            database='noc'
        )

    def ch_insert(self,*args):
         cursor1 = self.connection1.cursor()
         cursor2 = self.connection2.cursor()
         tz = timezone('Europe/Moscow')
         date = datetime.now(tz).strftime('%Y-%m-%d')
         timenow = datetime.now(tz).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
         query = "INSERT INTO stack (date, ts, metric_type, managed_object, member_name, member_id, status) VALUES "
         for data in self.mylist:
             member = data["obj_target"]
             managed_object = data["obj_bi_id"]
             for mem in member:
                 member = mem.keys()
                 stat = mem.values()
                 for m, s in zip(member, stat):
                     member_name = m
                     member_id = int(re.findall(r"Member_id:\d+", member_name)[0].split("Member_id:")[1])
                     status = int(s)
                     query += "".join(f"('{date}','{timenow}','',{managed_object}, '{member_name}', '{member_id}', {status}),")
         query = query.rstrip(",")
         query = (f"{query};")
         cursor1.execute(query)
         results1 = cursor1.fetchall()
         cursor2.execute(query)
         results2 = cursor2.fetchall()
         self.connection1.close()
         self.connection2.close()
