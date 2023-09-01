

from .psql_conn import postgresql_connections
from .forms import get_ch_tuples_location,get_par_tuples_location
from .connect_handler_dif import CONNECT_DEVICE


class CONNECT_HANDLER():

        """
        Class for prepare data before connection to device
        """

        def __init__(self, ip_address,platform,device_type,
                     location, location_add, device_role,tenants, management):

            self.ip_address = ip_address
            self.platform = platform
            self.device_type = device_type
            self.location = location
            self.location_add = location_add
            self.device_role = device_role
            self.tenants = tenants
            self.management = management

        def connect_handler_to_device(self, *args):

                    print('this is connecthadler_first!!!!')
                    ip_conn = self.ip_address.split('/')[0]
                    mask = self.ip_address.split('/')[1]
                    connecting = CONNECT_DEVICE()
                    conn_scheme = connecting.check_ssh(ip_conn)
                    if conn_scheme == 0:
                        print('Not connection to device!!!')
                    if conn_scheme == 'telnet':
                        print('Are you sure that use telnet!?')
                    if conn_scheme == 'ssh':
                        print("ssh is ok")

                    psql = postgresql_connections()
                    choices_platform = psql.postgre_conn_platform()
                    choices_location = get_par_tuples_location()
                    choices_location_add = get_ch_tuples_location()
                    choices_device_role = psql.postgre_conn_device_role()
                    choices_tenants = psql.postgre_conn_tenant()
                    choices_management = [(1,'Active'),(2,'Offline')]

                    result_location = False
                    if self.location_add == '':
                        result_locaction = False
                    elif self.location_add != '':
                        result_location = True
                        location_add = (int(self.location_add))
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
                        if l[0] == self.location:
                            location = l
                    print('this is connecthadler1!!!!')
                    for p in choices_platform:
                        if p[0] == self.platform:
                            platform = p
                    print('this is connecthadler2!!!!')
                    for dev_r in choices_device_role:
                        if dev_r[0] == self.device_role:
                            device_role = dev_r
                    for t in choices_tenants:
                        if t[0] == self.tenants:
                            tenants = t
                    for man in choices_management:
                        if man[0] == self.management:
                            management = man
                    if result_location == True:
                        location = location_add
                    elif result_location == False:
                        location = location
                    #print('this is connecthadler3!!!!')
                    #print(location)
                    site_name = psql.postgre_conn_site(location[0])[0]
                    #print(platform,device_role,tenants,management,self.device_type)
                    #print(manufacturer[1])
                    if platform[1] == "Huawei.VRP":
                         connection = CONNECT_DEVICE(ip_conn,mask,platform,site_name,
                                                    location,device_role,tenants,conn_scheme,management)
                         connection.conn_Huawei()
                    if platform[1] == "Juniper.JUNOS":
                         connection = CONNECT_DEVICE(ip_conn,mask,platform,site_name,
                                                    location,device_role,tenants,conn_scheme,management)
                         connection.conn_Juniper_rpc()


if __name__ == '__main__':
    connecting = CONNECT_HANDLER()
