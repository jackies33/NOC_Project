



# ---------------------------------------------------------------------
# Fortinet.Fortigate.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces


class Script(BaseScript):
    name = "Fortinet.Fortigate.get_interfaces"
    interface = IGetInterfaces
    pattern_ifaces = r'name:\s+(\S+).+status:\s+(up|down).+type:\s+(physical)'


    def execute_cli(self,snmp_interface = None):


        interfaces = []
        my_snmp_list = []

        for i,n in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1"]):
            snmp_iface = self.profile.convert_interface_name(n)
            i = str(i).split("1.3.6.1.2.1.31.1.1.1.1")[0]
            my_snmp_list +=[{"snmp_ifname":n,"snmp_index":i}]
            # ifOperStatus up(1)
        # print("\n\n\nTEXT!!!!!!\n\n\n")
        #print(my_snmp_list)
        try:
            self.cli("config global")
            v2 = self.cli("get system interface")
        except self.CLISyntaxError:
            return []


        if v2:
            matches_ifaces = re.findall(self.pattern_ifaces, v2)
            for match1 in matches_ifaces:
                ifname = match1[0]
                if_status = match1[1]
                if_type = match1[2]
                for n in my_snmp_list:
                    if n["snmp_ifname"] == ifname:
                        try:
                            ifindex = int(n["snmp_index"])
                            # print("\n\n\nText!!!!!!\n\n\n")
                            # print(ifindex)
                            # print("\n\n\nText!!!!!!\n\n\n")
                            a_stat = 'up'
                            status = 'up'
                            if if_status == 'up':
                                a_stat = True
                                status = True
                            elif if_status == 'down':
                                a_stat = True
                                status = False
                            mac = None
                            try:
                                v3 = self.cli(f"get hardware nic {ifname}")
                                matches_mac = re.findall("Permanent_HWaddr\s+\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}", v3)
                                for mac_f in matches_mac:
                                    mac = mac_f.split("Permanent_HWaddr")[1].split()[0]
                            except Exception as err:
                                print(err)
                            iface = {
                                "name": ifname,
                                "admin_status": a_stat,
                                "oper_status": status,
                                "description": '',
                                "mac": mac,
                                "type": if_type,
                                "enabled_protocols": [],
                                "snmp_ifindex": ifindex,
                                "subinterfaces": [],
                            }

                            interfaces += [iface]
                        except Exception as err:
                            print(err)
                    else:
                        pass






        return [{"interfaces": interfaces}]



