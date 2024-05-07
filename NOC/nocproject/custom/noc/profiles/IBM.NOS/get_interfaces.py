



# ---------------------------------------------------------------------
# IBM.NOS.get_interfaces
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
    name = "IBM.NOS.get_interfaces"
    interface = IGetInterfaces
    pattern_status_up = r'(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(up|down|disabled)\s+(.+)'

    def execute_cli(self,snmp_interface = None):



        interfaces = []
        my_snmp_list = []
        i = None
        portchannel_members = {}
        portchannel_interface = []
        for pc in self.scripts.get_portchannel():
            i = pc["interface"]
            t = pc["type"] == "L"
            portchannel_interface += [i]
            for m in pc["members"]:
                portchannel_members[m] = (i, t)
        for pcface in portchannel_interface:
                    iface = {
                        "name": pcface,
                        "type": "aggregated",
                        "subinterfaces": [],
                    }
                    interfaces += [iface]

        for i,n in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1"]):
            snmp_iface = self.profile.convert_interface_name(n)
            my_snmp_list +=[{"snmp_ifname":n,"snmp_index":i}]
            # ifOperStatus up(1)
        #print("\n\n\nTEXT!!!!!!\n\n\n")
        #print(my_snmp_list)
        rx_phy_mac = re.compile("^MAC address:\s+(?P<mac>\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2})\s+IP", re.MULTILINE)
        mac = None

        try:
            v1 = self.cli("show sys-info")
            match = rx_phy_mac.search(v1)
            if match:
                mac = match.group("mac")
            #print(mac)

        except self.CLISyntaxError:
            return []
        try:
            v2 = self.cli("show interface status")
        except self.CLISyntaxError:
            return []


        if v2:
            matches1 = re.findall(self.pattern_status_up, v2)
            for match1 in matches1:
                ifname = match1[0]
                ifindex = match1[1]
                #print("\n\n\nText!!!!!!\n\n\n")
                #print(ifindex)
                #print("\n\n\nText!!!!!!\n\n\n")
                status = match1[2]
                desc = match1[3]
                a_stat = 'up'
                if status == 'disabled':
                    a_stat = False
                    status = False
                elif status == 'up':
                    a_stat = True
                    status = True
                elif status == 'down':
                    a_stat = True
                    status = False
                for n in my_snmp_list:
                    if n["snmp_ifname"] == ifname:
                          ifindex = int(n["snmp_index"])
                iface = {
                    "name": ifname,
                    "admin_status": a_stat,
                    "oper_status": status,
                    "description": desc,
                    "mac": mac,
                    "type": "physical",
                    "enabled_protocols": [],
                    "snmp_ifindex": ifindex,
                    "subinterfaces": [],
                }
                if ifname in portchannel_members:
                    ai, is_lacp = portchannel_members[ifname]
                    iface["aggregated_interface"] = ai
                    iface["enabled_protocols"] += ["LACP"]
                    #iface["subinterfaces"][0].update({"enabled_afi": []})
                # Portchannel interface
                elif ifname in portchannel_interface:
                    iface["type"] = "aggregated"
                interfaces += [iface]
                # Portchannel member



        return [{"interfaces": interfaces}]



