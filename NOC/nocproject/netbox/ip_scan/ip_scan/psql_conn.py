
import psycopg2

class postgresql_connections():

                """
                Class for psql connection and collecting some data
                """

                conn = psycopg2.connect(
                    host="localhost",
                    database="netbox",
                    user="netbox",
                    password="P@ssw0rd",
                    sslmode='disable',
                )
                cur = conn.cursor()

                def postgre_conn_manufacturer(self):
                        self.cur.execute("SELECT id , slug FROM dcim_manufacturer;")
                        manafacturer = (self.cur.fetchall())

                        return manafacturer


                def postgre_conn_platform(self):
                        self.cur.execute("SELECT id , name FROM dcim_platform;")
                        platform = (self.cur.fetchall())

                        return platform


                def postgre_conn_device_type(self):
                        self.cur.execute("SELECT id , model FROM dcim_devicetype;")
                        device_type = (self.cur.fetchall())

                        return device_type


                def postgre_conn_site(self,id):
                        self.cur.execute(f"SELECT id , site_id FROM dcim_location WHERE id={id};")
                        site = (self.cur.fetchall())

                        return site

                def postgre_conn_locations(self):
                    self.cur.execute("SELECT id , name , parent_id FROM dcim_location;")
                    locations = (self.cur.fetchall())

                    return locations

                def postgre_conn_locations_add(self):
                        self.cur.execute("SELECT id , name , parent_id, level, tree_id FROM dcim_location;")
                        locations = (self.cur.fetchall())

                        return locations


                def postgre_conn_device_role(self):
                        self.cur.execute("SELECT id , name FROM dcim_devicerole;")
                        device_role = (self.cur.fetchall())

                        return device_role


                def postgre_conn_tenant(self):
                        self.cur.execute("SELECT id , name FROM tenancy_tenant;")
                        tenant = (self.cur.fetchall())

                        return tenant






if __name__ == '__main__':
      print('main_psql_conn.py')

