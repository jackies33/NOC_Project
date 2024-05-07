



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
from noc.sa.interfaces.igetinterfacestatusex import IGetInterfaceStatusEx


class Script(BaseScript):
    name = "Atlas.OS.get_interface_status_ex"
    interface = IGetInterfaceStatusEx
    pattern_status_up = r'(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(up|down|disabled)\s+(.+)'

    def execute_snmp(self, interface=None, **kwargs):
        # Get interface status
        ifaces = []
        # IF-MIB::ifName, IF-MIB::ifOperStatus
        interfaces = []
        list_slots_id = []
        for snmp in self.snmp.get_tables(["1.3.6.1.4.1.39433.1.4"]):
            n = str(snmp[0])
            v = str(snmp[1])
            value = re.findall("ten\d+|evstc\d+|emstc\d+", v)
            if value != []:
                value = value[0]
                number_of_slot = n[-1]
                list_slots_id.append({'value': value, 'number_of_slot': number_of_slot})
        for slot in list_slots_id:
            value_main = re.findall("ten\d+", slot['value'])
            if value_main != []:
                value_main = value_main[0]
                main_number_of_slot = slot['number_of_slot']
                for r in range(67, 73):
                    ifname = self.snmp.get(f"1.3.6.1.4.1.39433.1.6.1.3.{main_number_of_slot}.3.{r}")
                    try:
                        ifname = ifname.split("Ln")[0]
                    except Exception:
                        pass
                    status = self.snmp.get(f"1.3.6.1.4.1.39433.1.6.1.5.{main_number_of_slot}.3.{r}")
                    if status == '1':
                        status = False
                    elif status == '2':
                        status = True
                    iface =  {"interface": ifname, 'admin_status': status ,"oper_status": status},#"in_speed": 100000000,
                              #"out_speed": 100000000}
                    ifaces += [iface]


        return ifaces

