

import psycopg2
from pymongo import MongoClient
from datetime import datetime
import clickhouse_driver
from pytz import timezone
from my_pass import pass_noc,user_noc

class PSQL_CONN():

                """
                Class for psql connection and collecting some data
                """

                def __init__(self,list1=None,list2=None):
                        self.list1=list1
                        self.list2 = list2
                        self.conn = psycopg2.connect(
                            host="10.50.50.170",
                            database="noc",
                            user=user_noc,
                            password=pass_noc,
                            sslmode='disable',
                        )
                        self.cur = self.conn.cursor()


                def postgre_conn_inv(self,*args):
                        self.cur.execute(f"select id,name,address,bi_id,segment from sa_managedobject where segment IN ({self.list1});")
                        tuple = (self.cur.fetchall())
                        return tuple

                def get_id(self, *args):
                        self.cur.execute(f"select id from sa_managedobjectprofile where name IN ({self.list2});")
                        tuple = (self.cur.fetchall())
                        return tuple


class MONGO():

      """class for connection and recieve data from mongo DB"""

      def __init__(self,id1=None,id_list2=None):
          self.id1=id1
          self.id_list2=id_list2



      def get_alarm(self):
          client = MongoClient(f'mongodb://noc:{user_noc}@kr01-mongodb01:27017/{pass_noc}')
          db = client['noc']
          collection = db['noc.alarms.active']
          find = collection.find()
          list_for_alarm = []
          for dict in find:
              vars = dict['vars']
              manged_object = dict["managed_object"]
              if vars == {}:
                  continue
              elif vars != {}:
                  inteface = vars["interface"]
                  if inteface != '':
                      if manged_object in list_for_alarm:
                          continue
                      elif manged_object not in list_for_alarm:
                          list_for_alarm.append(manged_object)
                  else:
                      continue
          return list_for_alarm

      def get_segment_id(self, *args):
          name = ''
          client = MongoClient(f'mongodb://noc:{user_noc}@kr01-mongodb01:27017/{pass_noc}')
          db = client['noc']
          collection = db['noc.networksegments']
          result = []
          for name in self.id_list2:
              find = collection.find_one({"name": name})
              if find:
                  id = str(find.get("_id"))
                  result.append({"name": name, "id": id})
          return result


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

    def ch_insert(self, *args):
        cursor1 = self.connection1.cursor()
        cursor2 = self.connection2.cursor()
        tz = timezone('Europe/Moscow')
        date = datetime.now(tz).strftime('%Y-%m-%d')
        timenow = datetime.now(tz).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO disp_icmp (date, ts, metric_type, managed_object, mo_name, mo_ip, mo_segment, status) VALUES "
        for data in self.mylist:
            status = data["obj_result"]
            bi_id = data["obj_bi_id"]
            obj_name = data["obj_name"]
            obj_segment = data["obj_segment"]
            obj_ip = data["obj_ip_address"]
            query += "".join(f"('{date}','{timenow}','',{bi_id}, '{obj_name}', '{obj_ip}', '{obj_segment}', {status}),")
        query = query.rstrip(",")
        query = (f"{query};")
        cursor1.execute(query)
        results1 = cursor1.fetchall()
        cursor2.execute(query)
        results2 = cursor2.fetchall()
        self.connection1.close()
        self.connection2.close()


