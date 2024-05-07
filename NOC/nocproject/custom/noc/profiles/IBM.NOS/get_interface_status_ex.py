



# ---------------------------------------------------------------------
# IBM.NOS.get_interface_status
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
    name = "IBM.NOS.get_interface_status_ex"
    interface = IGetInterfaceStatusEx
    pattern_status_up = r'(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(up|down|disabled)\s+(.+)'

    def execute_snmp(self, interface=None, **kwargs):
        # Get interface status
        r = []
        # IF-MIB::ifName, IF-MIB::ifOperStatus
        for i, n, s in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.2.2.1.8"]):
            iface = self.profile.convert_interface_name(n)
            # ifOperStatus up(1)
            #print("\n\n\ntext\n\n\n")
            #print(i,n,s)
            #print("\n\n\ntext\n\n\n")
            if interface and interface == iface:
                return [{"interface": iface, "status": int(s) == 2}]
            if not self.profile.convert_interface_name(n):
                continue
            r += [{"interface": iface, "status": int(s) == 2}]
        return r


    """
    def execute(self):
        r = []
        try:
            v = self.cli("show interface status")
        except self.CLISyntaxError:
            return []
        if v:
            matches1 = re.findall(self.pattern_status_up, v)
            for match1 in matches1:
                ifname = match1[0]
                status = match1[2]
                if status == 'up':
                    status = True
                r += [
                        {"interface": ifname, "status": status == 1}
                ]
        return r


    """



