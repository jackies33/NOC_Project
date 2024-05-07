




# ---------------------------------------------------------------------
# Atlas.OS.get_interface_status
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------


# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfacestatus import IGetInterfaceStatus


class Script(BaseScript):
    name = "Atlas.OS.get_interface_status"
    interface = IGetInterfaceStatus
    pattern_status_up = r'(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(up|down|disabled)\s+(.+)'

    def execute_snmp(self, interface=None, **kwargs):
        # Get interface status
        ifaces = []
        list_collect_data = []
        list_members = []
        for snmp in self.snmp.get_tables(["1.3.6.1.4.1.39433.1.4"]):
            n = str(snmp[0])
            v = str(snmp[1])
            value = re.findall("ten\d+", v)
            if value != []:
                value = value[0]
                if value != []:
                    value = value[0]
                    number_of_slot = n[-1]
                    list_members.append(number_of_slot)
        for number_of_slot in list_members:
            for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.3.{number_of_slot}.3"]):
                if "Cl1PortState" in str(snmp[1]):
                    interface_name = f"Client/{number_of_slot}/{snmp[1].split('Cl1')[0]}"
                    ifindex = snmp[0]
                    list_collect_data.append({"ifname": interface_name, "ifindex": ifindex})
                elif "Ln1PortState" in str(snmp[1]):
                    interface_name = f"Network/{number_of_slot}/{snmp[1].split('Ln1')[0]}"
                    ifindex = snmp[0]
                    list_collect_data.append({"ifname": interface_name, "ifindex": ifindex})
            for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.5.{number_of_slot}.3"]):
                for dict in list_collect_data:
                    if str(dict['ifindex']) == str(snmp[0]):
                        status = str(snmp[1])
                        dict.update({"status": status})
            for res in list_collect_data:

                ifname = res['ifname']
                try:
                    status = ["status"]
                except Exception as err:
                    status = None
                if status == '1':
                    status = False
                elif status == '2':
                    status = True
                iface =  {"interface": ifname, "status": True}#status}
                ifaces += [iface]


        return ifaces

