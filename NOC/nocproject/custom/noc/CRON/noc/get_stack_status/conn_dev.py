

from jnpr.junos import Device
from concurrent.futures import ThreadPoolExecutor
from my_pass import mylogin,mypass
import logging
import datetime

class CONNECT_DEVICE():
    """
    Class for connection to different device
    """

    def __init__(self, devices):
        self.devices = devices
        # self.platform = "default"


    def jun_rpc(self, device_dict):
        ip_conn = device_dict['obj_ip']
        try:
            dev = Device(host=ip_conn, user=mylogin, password=mypass)
            dev.open()
            vc_info = dev.rpc.get_virtual_chassis_information()
            members = vc_info.findall('.//member')
            result = []
            for member in members:
                member_id = int(member.find('member-id').text)
                member_serial_number = member.find('member-serial-number').text
                status = member.find('member-status').text
                my_dict = {"member_id": member_id, "member_sn": member_serial_number, "status": status}
                result.append(my_dict)
            return result
        except Exception as e:
            print(f"Error {e}")
            return None

    def conn_Juniper(self, *args):
        data = []
        with ThreadPoolExecutor(max_workers=30) as executor:
            result = executor.map(self.jun_rpc, self.devices)
            for device, output in zip(self.devices, result):
                try:
                    if output != '' or [] or None:
                        data2 = []
                        data3 = []
                        data4 = []
                        for target in output:
                            member = int(target['member_id'])
                            status = target['status']
                            sn = target['member_sn']
                            if status == "Mismatch":
                                data3.append({f"Member_id:{member},S/N:{sn}": 0})
                            elif status == "Prsnt":
                                data3.append({f"Member_id:{member},S/N:{sn}": 1})
                        data4.extend(data3)
                        data5 = ({"obj_id": device["obj_id"],
                                  "obj_ip": device["obj_ip"],
                                  "obj_name": device["obj_name"],
                                  "obj_prof_id": device["obj_prof_id"],
                                  "obj_vendor": device["obj_vendor"],
                                  "obj_vendor_id": device["obj_vendor_id"],
                                  "obj_bi_id": device["obj_bi_id"],
                                  "obj_target": data4})
                        data2.append(data5)
                        data.extend(data2)

                    elif output == '' or [] or None:
                        continue

                except TypeError as err:
                    logging.warning(f'________\n\n\n{datetime.datetime.now()}   ----   {err}\n\n\n_________')
                except Exception as err:
                    logging.warning(f'________\n\n\n{datetime.datetime.now()}   ----   {err}\n\n\n_________')
        return data

