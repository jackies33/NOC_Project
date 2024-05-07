


import psycopg2
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import re
import clickhouse_driver
from pytz import timezone
from my_pass import pass_noc,user_noc
import logging


class PSQL_CONN():

                """
                Class for psql connection and collecting some data
                """

                def __init__(self,id1=None,list1=None):
                        self.id1=id1
                        self.list1 = list1
                        self.conn = psycopg2.connect(
                            host="10.50.74.171",
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
          #collection = self.db[f'noc.vendors.find({"_id" : ObjectId("{self.id1}")})']
          name = ''
          try:
              client = MongoClient(f'mongodb://noc:{user_noc}@kr01-main-noc:27017/{pass_noc}')
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
          except Exception as err:
              logging.warning(f'________\n\n\n{datetime.now()}   ----   {err}\n\n\n_________')


def get_bi_id(self,*args):
          name = ''
          try:
              client = MongoClient(f'mongodb://noc:{user_noc}@kr01-main-noc:27017/{pass_noc}')
              db = client['noc']
              collection = db['ds_managedobject']
              id = int(self.id2)
              #print(id)
              find = collection.find({"_id" : id})
              for d in find:
                 print(d)
              #print(find)
              result = ''
              #if find:
               #   quot= find.get("data", {}.get("name"))
                #  result = (re.findall('"bi_id":\d+', quot)[0].split('"bi_id":'))[1]
              #return result
          except Exception as err:
              logging.warning(f'________\n\n\n{datetime.now()}   ----   {err}\n\n\n_________')


class CH():

    """Class for connection and execute command to CH server"""

    def __init__(self,mylist):
        self.mylist = mylist
        self.connection1 = clickhouse_driver.connect(
            host='10.50.74.171',
            port=9000,
            user=user_noc,
            password=pass_noc,
            database='noc'
        )

    def ch_insert(self,*args):
        try:

             cursor1 = self.connection1.cursor()
             tz = timezone('Europe/Moscow')
             date = datetime.now(tz).strftime('%Y-%m-%d')
             timenow = datetime.now(tz).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
             query = "INSERT INTO stack (date, ts, metric_type, managed_object, member_name, member_id, status) VALUES "
             for data in self.mylist:
                 try:
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
                 except Exception as err:
                     logging.warning(f'________\n\n\n{datetime.now()}   ----   {err}\n\n\n_________')
             query = query.rstrip(",")
             query = (f"{query};")
             #print(query)
             #tz = timezone('Europe/Moscow')
             #timenow = datetime.now(tz).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
             #print(timenow)
             cursor1.execute(query)
             results1 = cursor1.fetchall()
             #for row1,row2 in zip(results1,results2):
                  #return row1,row2
             self.connection1.close()
        except Exception as err:
             logging.warning(f'________\n\n\n{datetime.now()}   ----   {err}\n\n\n_________')


