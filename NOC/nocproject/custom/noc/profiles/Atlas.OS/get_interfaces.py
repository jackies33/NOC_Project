


# ---------------------------------------------------------------------
# Atlas.OS.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
import re

class Script(BaseScript):
    name = "Atlas.OS.get_interfaces"
    interface = IGetInterfaces


    def execute_snmp(self,snmp_interface = None):

        interfaces = []
        list_collect_data = []
        list_members = []
        for snmp in self.snmp.get_tables(["1.3.6.1.4.1.39433.1.4"]):
            n = str(snmp[0])
            v = str(snmp[1])
            value = re.findall("ten\d+", v)  # ("ten\d+|evstc\d+|emstc\d+", v)
            if value != []:
                value = value[0]
                number_of_slot = n[-1]
                list_members.append(number_of_slot)
        for number_of_slot in list_members:
                for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.3.{number_of_slot}.3"]):
                    if "Cl1PortState" in str(snmp[1]):
                        interface_name = f"Client/{number_of_slot}/{snmp[1].split('Cl1')[0]}"
                        ifindex = snmp[0]
                        list_collect_data.append({"ifname":interface_name,"ifindex":ifindex})
                    elif "Ln1PortState" in str(snmp[1]):
                        interface_name = f"Network/{number_of_slot}/{snmp[1].split('Ln1')[0]}"
                        ifindex = snmp[0]
                        list_collect_data.append({"ifname": interface_name, "ifindex": ifindex})
                for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.5.{number_of_slot}.3"]):
                    for dict in list_collect_data:
                        if str(dict['ifindex']) == str(snmp[0]):
                            status = str(snmp[1])
                            dict.update({"status":status})
                index_description = 67
                for r in range(13, 19):
                    descr = self.snmp.get(f"1.3.6.1.4.1.39433.1.6.1.5.{number_of_slot}.1.{r}")
                    for dict in list_collect_data:
                        if str(dict['ifindex']) == str(r):
                            dict.update({"description": descr})
                    index_description = index_description + 1
                for res in list_collect_data:
                    status = res["status"]
                    if status == '1':
                        status = False
                    elif status == '2':
                        status = True
                    try:
                        descr = res['description']
                    except Exception as err:
                        descr = ''
                    ifindex = res['ifindex']
                    ifname = res["ifname"]
                    iface = {
                        "name": ifname,
                        "admin_status": True,
                        "oper_status": status,
                        "description": descr,
                        "mac": None,
                        "type": "physical",
                        "enabled_protocols": [],
                        "snmp_ifindex": ifindex,
                        "subinterfaces": [],
                    }
                    interfaces += [iface]

        return [{"interfaces": interfaces}]


