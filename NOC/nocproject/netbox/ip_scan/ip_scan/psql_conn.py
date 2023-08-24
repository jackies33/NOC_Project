
import psycopg2

class postgresql_connections():

                conn = psycopg2.connect(
                    host="localhost",
                    database="netbox",
                    user="netbox",
                    password="P@ssw0rd",
                    sslmode='disable',
                )

                def postgre_conn_manufacturer(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id , slug FROM dcim_manufacturer;")
                        manafacturer = (cur.fetchall())

                        return manafacturer


                def postgre_conn_platform(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id , name FROM dcim_platform;")
                        platform = (cur.fetchall())

                        return platform


                def postgre_conn_device_type(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id , model FROM dcim_devicetype;")
                        device_type = (cur.fetchall())

                        return device_type


                def postgre_conn_site(self,id):
                        cur = self.conn.cursor()
                        cur.execute(f"SELECT id , site_id FROM dcim_location WHERE id={id};")
                        site = (cur.fetchall())

                        return site

                def postgre_conn_locations(self):
                    cur = self.conn.cursor()
                    cur.execute("SELECT id , name , parent_id FROM dcim_location;")
                    locations = (cur.fetchall())

                    return locations

                def postgre_conn_locations_add(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id , name , parent_id, level, tree_id FROM dcim_location;")
                        locations = (cur.fetchall())

                        return locations


                def postgre_conn_device_role(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id , name FROM dcim_devicerole;")
                        device_role = (cur.fetchall())

                        return device_role


                def postgre_conn_tenant(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id , name FROM tenancy_tenant;")
                        tenant = (cur.fetchall())

                        return tenant




if __name__ == '__main__':
      print('main_psql_conn.py')

