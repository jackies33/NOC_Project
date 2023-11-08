
import psycopg2
from .my_pass import login_netbox_psql,netbox_pass


class postgresql_connections():

                """
                Class for psql connection and collecting some data
                """
                def __init__(self,id_site=None,id_platform=None):
                    self.id_site=id_site
                    self.id_platform =id_platform

                conn = psycopg2.connect(
                    host="localhost",
                    database=login_netbox_psql,
                    user=login_netbox_psql,
                    password=netbox_pass,
                    sslmode='disable',
                )
                cur = conn.cursor()


                def postgre_conn_platform(self,*args):
                        self.cur.execute(f"SELECT id , name FROM dcim_platform where id = '{self.id_platform}';")
                        platform = (self.cur.fetchall())

                        return platform


                def postgre_conn_device_type(self):
                        self.cur.execute("SELECT id , model FROM dcim_devicetype;")
                        device_type = (self.cur.fetchall())

                        return device_type


                def postgre_conn_site(self,*args):
                        self.cur.execute(f"SELECT id , site_id FROM dcim_location WHERE id={self.id_site};")
                        site = (self.cur.fetchall())

                        return site



if __name__ == '__main__':
      print('main_psql_conn.py')

