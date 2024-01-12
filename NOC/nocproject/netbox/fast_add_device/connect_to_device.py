

from .connect_handler_dif import CONNECT_HANDLER
import pynetbox
from .my_pass import netbox_url,netbox_api_token

class CONNECT_DEVICE():

        """
        Class for prepare data before connection to device
        """

        def __init__(self, ip_address,platform,
                     device_role,tenants,location,racks):

            self.ip_address = ip_address
            self.platform = platform
            self.device_role = device_role
            self.tenants = tenants
            self.location = location
            self.racks = racks

        def prepare_for_connection(self, *args):
                    ip_conn = self.ip_address.split('/')[0]
                    mask = self.ip_address.split('/')[1]
                    connecting = CONNECT_HANDLER()
                    conn_scheme = connecting.check_ssh(ip_conn)
                    if conn_scheme == 0:
                        print('No connection to device!!!')
                        return [False, "No connection to device! "]
                    if conn_scheme == 'telnet':
                        conn_scheme = '2'
                        print('Are you sure that use telnet!?')
                    if conn_scheme == 'ssh':
                        conn_scheme = '1'
                        print("ssh is ok")

                    nb = pynetbox.api(url=netbox_url, token=netbox_api_token)
                    nb.http_session.verify = False
                    platform_main = nb.dcim.platforms.get(id=self.platform)
                    platform = str(platform_main)
                    platform_id = int(platform_main.id)
                    location_main = nb.dcim.locations.get(id=self.location)
                    site_name = int(location_main.site.id)
                    result = []
                    if platform == "Huawei.VRP":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform_id,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.racks)
                         result = connection.conn_Huawei()
                    if platform == "Juniper.JUNOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform_id,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.racks)
                         result = connection.conn_Juniper_rpc()
                    if platform == "Cisco.IOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform_id,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.racks)
                         result = connection.conn_Cisco_IOS()
                    if platform == "IBM.NOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform_id,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.racks)
                         result = connection.conn_IBM_lenovo_sw()
                    if platform == "Cisco.NXOS":
                         connection = CONNECT_HANDLER(ip_conn,mask,platform_id,site_name,self.location,self.device_role,self.tenants,conn_scheme,self.racks)
                         result = connection.conn_Cisco_NXOS()
                    if platform == "Aruba.ArubaOS":
                        connection = CONNECT_HANDLER(ip_conn, mask, platform_id, site_name, self.location,self.device_role, self.tenants, conn_scheme,self.racks)
                        result = connection.conn_AWMP()
                    if platform == "Fortinet.Fortigate":
                        connection = CONNECT_HANDLER(ip_conn, mask, platform_id, site_name, self.location,self.device_role, self.tenants, conn_scheme,self.racks)
                        result = connection.conn_FortiGate()
                    if platform == "OS.Linux":
                        connection = CONNECT_HANDLER(ip_conn, mask, platform_id, site_name, self.location,self.device_role, self.tenants, conn_scheme,self.racks)
                        result = connection.conn_OS_Linux()
                    return result


if __name__ == '__main__':
    print("__main__")
