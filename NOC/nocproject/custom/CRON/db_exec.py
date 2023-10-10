


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
          #collection = self.db[f'noc.vendors.find({"_id" : ObjectId("{self.id1}")})']
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
                     query = f"INSERT INTO stack (date, ts, metric_type, managed_object, member_name, member_id, status) VALUES ('{date}'," \
                             f"'{timenow}', '', {managed_object}, '{member_name}', {member_id}, {status});"
                     #print(query)
                     cursor1.execute(query)
                     results1 = cursor1.fetchall()
                     cursor2.execute(query)
                     results2 = cursor2.fetchall()
                     #for row1,row2 in zip(results1,results2):
                      #    return row1,row2
         self.connection1.close()

"""
if __name__ == '__main__':
   mylist =  [{'obj_id': 155, 'obj_ip': '10.100.9.43', 'obj_name': 'kubik-v-4-1', 'obj_prof_id': 14,
               'obj_vendor': 'Juniper Networks', 'obj_vendor_id': '64c8db6a498777ecdeb457cd',
               'obj_bi_id': 5596169363328238258, 'obj_target': [{'Member_id:0,S/N:CT0214420764': 1},
                                                                {'Member_id:1,S/N:CT0214420405': 1},
                                                                {'Member_id:2,S/N:CT0214420700': 1},
                                                                {'Member_id:3,S/N:CT0217370727': 1}]},
              {'obj_id': 151, 'obj_ip': '10.100.9.131', 'obj_name': 'kubik-v-11', 'obj_prof_id': 14,
               'obj_vendor': 'Juniper Networks', 'obj_vendor_id': '64c8db6a498777ecdeb457cd',
               'obj_bi_id': 1926171014946576163, 'obj_target': [{'Member_id:0,S/N:CT0217370882': 1},
                                                                {'Member_id:1,S/N:CT0217370551': 1},
                                                                {'Member_id:2,S/N:CT0217370633': 1}]}]

   clickhouse = CH(mylist)
   clickhouse.ch_insert()

"""