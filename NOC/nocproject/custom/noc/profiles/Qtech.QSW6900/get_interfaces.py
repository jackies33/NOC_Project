

# ---------------------------------------------------------------------
# Qtech.QSW6900.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.ip import IPv4
from noc.core.ip import IPv6


class Script(BaseScript):
    """
    Qtech.QSW6900.get_interfaces
    """

    name = "Qtech.QSW6900.get_interfaces"
    interface = IGetInterfaces

    rx_interface_l2_main = re.compile(
        r"^Index\(dec\):(?P<index>\d+?).+\n(?P<interface>\S+\s+(\d+|\d+/\d+)?) is (?P<status>(UP|DOWN)?).+\n"
        r".+, address is (?P<mac_address>\S+).+\n(\s+)Description: (?P<description>.+?)\n", re.MULTILINE)

    types = {
        "e": "physical",  # FastEthernet
        "g": "physical",  # GigabitEthernet
        "t": "physical",  # TenGigabitEthernet
    }
    def execute(self,snmp_interface=None):

        interfaces = []
        list_for_add = []
        #"""
        try:
            for i, n, s, d in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.2.2.1.8","1.3.6.1.2.1.31.1.1.1.18"]):
                iface_name = self.profile.convert_interface_name(str(n))
                iface_index = int(i)
                iface_status = int(s)
                iface_description = str(d)
                if iface_status == 1:
                    iface_status = True
                elif iface_status == 2:
                    iface_status = False
                list_for_add.append({"ifindex": iface_index, "ifname": iface_name, "status":
                    iface_status,"description":iface_description})
        except Exception:
            pass

        #"""
        try:
            output_mac = self.cli(" show sysmac")
            mac = re.findall(f"\S+\.\S+\.\S+", output_mac)[0]
            #for match in self.rx_interface_l2_main.finditer(output_main):
            #    ifname = match.group('interface')
            #    stat = match.group("status").lower()
            #    description = match.group("description")
            #    mac =match.group("mac_address")
            #    ifindex = match.group("index")
            #    iface = {
            #        "name": ifname,
            #        "type": "physical",
            #        "admin_status": stat,
            #        "oper_status": stat,
            #        "description": description,
            #        "mac": mac,
            #        "enabled_protocols": [],
            #        "snmp_ifindex": ifindex,
            #        "subinterfaces": []
            #    }
            for l in list_for_add:
                if l["ifname"] == None or l["ifname"] == '' :
                    continue
                iface = {
                    "name": l['ifname'],
                    "type": "physical",
                    "admin_status": l['status'],
                    "oper_status": l['status'],
                    "description":l['description'],
                    "mac": mac,
                    "enabled_protocols": [],
                    "snmp_ifindex": l['ifindex'],
                    "subinterfaces": [],
                }

                interfaces.append(iface)
            return [{"interfaces": interfaces}]
        except Exception as err:
            print(err)




