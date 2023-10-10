

#from pprint import pprint
#from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from my_pass import mylogin,mypass
from itertools import repeat
import logging
from netmiko import ConnectHandler, NetMikoAuthenticationException
import re

class CONNECT_DEVICE():
    """
    Class for connection to different device
    """

    def __init__(self, devices):
        self.devices = devices
        # self.platform = "default"

    """
    logging.getLogger('paramiko').setLevel(logging.WARNING)

    logging.basicConfig(
        format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO,
    )
    """

    def template_conn(self, ip,device_type):
        host1 = ''
        if device_type == 'Huawei Technologies Co.':
            host1 = {

                "host": ip,
                "username": mylogin,
                "password": mypass,
                "device_type": 'huawei',
                "global_delay_factor": 0.5,
            }
        if device_type == 'Juniper Networks':
            host1 = {

                "host": ip,
                "username": mylogin,
                "password": mypass,
                "device_type": 'juniper_junos',
                "global_delay_factor": 0.5,
            }
        return host1


    def send_show(self,device_dict, command):
        #start_msg = '===> {} Connection: {}'
        #received_msg = '<=== {} Received:   {}'
        ip = device_dict['obj_ip']
        device_type = device_dict['obj_vendor']
        #logging.info(start_msg.format(datetime.now().time(), ip))
        host1 = self.template_conn(ip,device_type)

        try:
            with ConnectHandler(**host1) as ssh:
                result = ssh.send_command(command)
                #logging.info(received_msg.format(datetime.now().time(), ip))
                ssh.disconnect()
            return result
        except NetMikoAuthenticationException as err:
            logging.warning(err)


    def comm_Juniper(self,*args):
        data = []
        command = "show virtual-chassis"
        with ThreadPoolExecutor(max_workers=5) as executor:
            result = executor.map(self.send_show, self.devices, repeat(command))
            for  device , output in zip(self.devices,result):
                find = re.findall(r'\(FPC \d+\)  (?:Prsnt|Mismatch)    \S+', output)
                data2 = []
                data3 = []
                data4 = []
                for target in find:
                    memb = re.findall(r"\(FPC \d+\)", target)[0]
                    member = int(re.findall(r"\d+", memb)[0])
                    if "Mismatch" in target:
                        sn = target.split("Mismatch    ")[1]
                        #print(f"\nAlarm! Member {member} S/N:{sn} is DOWN")
                        data3.append({f"Member_id:{member},S/N:{sn}":0})
                    elif "Prsnt" in target:
                        sn = target.split("Prsnt    ")[1]
                        #print(f"\nMember {member} S/N:{sn} is UP")
                        data3.append({f"Member_id:{member},S/N:{sn}":1})
                #data4.extend([f"{device['obj_ip']}",data3])
                data4.extend(data3)
                data5 = ({"obj_id":device["obj_id"],
                          "obj_ip":device["obj_ip"],
                          "obj_name":device["obj_name"],
                             "obj_prof_id":device["obj_prof_id"],
                          "obj_vendor":device["obj_vendor"],
                          "obj_vendor_id":device["obj_vendor_id"],
                          "obj_bi_id":device["obj_bi_id"],
                          "obj_target":data4})
                data2.append(data5)
                data.extend(data2)
        return data


"""
if __name__ == '__main__':
    devices = [{'obj_id': 155, 'obj_name': 'kubik-v-4-1', 'obj_ip': '10.100.9.43', 'obj_prof_id': 14, 'obj_vendor': 'Juniper Networks',
                'obj_vendor_id': '64c8db6a498777ecdeb457cd',
                'obj_bi_id': 5596169363328238258}, {'obj_id': 151, 'obj_name': 'kubik-v-11',
                'obj_ip': '10.100.9.131', 'obj_prof_id': 14, 'obj_vendor': 'Juniper Networks',
                'obj_vendor_id': '64c8db6a498777ecdeb457cd', 'obj_bi_id': 1926171014946576163}]

        #{"ip": "10.100.9.131", "device_type": "juniper_junos"},
        #{"ip": "10.100.9.43", "device_type": "juniper_junos"},
    exec = CONNECT_DEVICE(devices)
    result = exec.comm_Juniper()
    print(result)
"""