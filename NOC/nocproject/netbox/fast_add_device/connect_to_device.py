


from .psql_conn import postgresql_connections
from .connect_handler_dif import CONNECT_HANDLER


class CONNECT_DEVICE():

        """
        Class for prepare data before connection to device
        """

        def __init__(self, ip_address,platform,device_type,
                     device_role,tenants,location,management):

            self.ip_address = ip_address
            self.platform = platform
            self.device_type = device_type
            self.device_role = device_role
            self.tenants = tenants
            self.location = location
            self.management = management

        def prepare_for_connection(self, *args):
                    ip_conn = self.ip_address.split('/')[0]
                    mask = self.ip_address.split('/')[1]
                    connecting = CONNECT_HANDLER()
                    conn_scheme = connecting.check_ssh(ip_conn)
                    if conn_scheme == 0:
                        print('Not connection to device!!!')
                    if conn_scheme == 'telnet':
                        print('Are you sure that use telnet!?')
                    if conn_scheme == 'ssh':
                        print("ssh is ok")
                    psql = postgresql_connections(self.location,self.platform)
                    platform = psql.postgre_conn_platform()[0]
                    #choices_management = [(1,'Active'),(2,'Offline')]
                    site_name = psql.postgre_conn_site()
                    result = []
                    if platform[1] == "Huawei.VRP":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.management)
                         result = connection.conn_Huawei()
                    if platform[1] == "Juniper.JUNOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.management)
                         result = connection.conn_Juniper_rpc()
                    if platform[1] == "IBM.NOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.management)
                         result = connection.conn_IBM_lenovo_sw()
                    if platform[1] == "Cisco.NXOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.management)
                         result = connection.conn_Cisco_NXOS()
                    if platform[1] == "Aruba.ArubaOS":
                        connection = CONNECT_HANDLER(ip_conn, mask, platform, site_name, self.location,self.device_role, self.tenants, conn_scheme, self.management)
                        result = connection.conn_AWMP()
                    if platform[1] == "Fortinet.Fortigate":
                        connection = CONNECT_HANDLER(ip_conn, mask, platform, site_name, self.location,self.device_role, self.tenants, conn_scheme, self.management)
                        result = connection.conn_FortiGate()
                    return result


if __name__ == '__main__':
    print("__main__")
