
import subprocess
from concurrent.futures import ThreadPoolExecutor


class ICMP():

    def __init__(self,ip_list):
        self.ip_list=ip_list

    def icmp_ping(self,my_dict):
        name = my_dict["obj_name"]
        my_ip = my_dict["obj_ip"]
        my_id = my_dict["obj_id"]
        my_segment = my_dict["obj_segment_name"]
        my_bi_id = my_dict["obj_bi_id"]
        with open('/dev/null', 'w') as devnull:
           response = subprocess.call(["ping", "-c", "1", "-W", "1" ,my_ip], stdout=devnull, stderr=subprocess.STDOUT)
           if response == 0:
                        icmp_result = {"obj_id":my_id,"obj_ip_address":my_ip,"obj_name":name,"obj_segment":my_segment,"obj_bi_id":my_bi_id,"obj_result":3}
           else:
                        for i in range(2):
                            if response == 0:
                                icmp_result = {"obj_id":my_id,"obj_ip_address":my_ip,"obj_name":name,"obj_segment":my_segment,"obj_bi_id":my_bi_id,"obj_result":3}
                                break
                            else:
                                icmp_result = {"obj_id":my_id,"obj_ip_address":my_ip,"obj_name":name,"obj_segment":my_segment,"obj_bi_id":my_bi_id,"obj_result":1}
        return icmp_result

    def executer_icmp(self,*args):
        result = []
        with ThreadPoolExecutor() as executor:
          for my_dict in self.ip_list:
                result.append(executor.submit(self.icmp_ping, my_dict))
        return result


