

from .psql_conn import postgresql_connections
from .forms import IpAddressForm,get_ch_tuples_location,get_par_tuples_location
from .connect_handler_dif import conn_device #conn_Huawei,conn_Juniper_rpc,check_ssh



def connect_handler_to_device(ip_address,platfrom,device_type,location,location_add,device_role,tenants,management):

            connect_to_dev = conn_device()
            print('this is connecthadler_first!!!!')
            ip_conn = ip_address.split('/')[0]
            mask = ip_address.split('/')[1]
            conn_scheme = connect_to_dev.check_ssh(ip_conn)
            if conn_scheme == 0:
                print('Not connection to device!!!')
            if conn_scheme == 'telnet':
                print('Are you sure that use telnet!?')
            if conn_scheme == 'ssh':
                print("ssh is ok")

            psql = postgresql_connections()
            choices_platfrom = psql.postgre_conn_platform()
            choices_location = get_par_tuples_location()
            choices_location_add = get_ch_tuples_location()
            choices_device_role = psql.postgre_conn_device_role()
            choices_tenants = psql.postgre_conn_tenant()
            choices_management = [(1,'Active'),(2,'Offline')]

            result_location = False
            if location_add == '':
                result_locaction = False
            elif location_add != '':
                result_location = True
                location_add = (int(location_add))
                for l_a in choices_location_add:
                    if l_a[0] == location_add:
                        location_add = l_a

            print('this is connecthadler!!!!')

            """
            for m in choices_manufacturer:
                if m[0] == manufacturer:
                    manufacturer = m
            for dev_t in choices_device_type:
                if dev_t[0] == device_type1:
                    device_type = dev_t
            for s in choices_site_name:
                if s[0] == site_name:
                    site_name = s
            """
            for l in choices_location:
                if l[0] == location:
                    location = l
            for p in choices_platfrom:
                if p[0] == platfrom:
                    platfrom = p
            for dev_r in choices_device_role:
                if dev_r[0] == device_role:
                    device_role = dev_r
            for t in choices_tenants:
                if t[0] == tenants:
                    tenants = t
            for man in choices_management:
                if man[0] == management:
                    management = man
            if result_location == True:
                location = location_add
            elif result_locaction == False:
                location = location
            connPSQL = postgresql_connections()
            site_name = connPSQL.postgre_conn_site(location[0])[0]
            #print(manufacturer[1])
            if platfrom[1] == "Huawei.VRP":
                 connect_to_dev.conn_Huawei(ip_conn,mask,platfrom,device_type,site_name,location,device_role,tenants,conn_scheme,management)
            if platfrom[1] == "Juniper.JUNOS":
                 connect_to_dev.conn_Juniper_rpc(ip_conn,mask,platfrom,device_type,site_name,location,device_role,tenants,conn_scheme,management)


if __name__ == '__main__':
     connect_handler_to_device()
