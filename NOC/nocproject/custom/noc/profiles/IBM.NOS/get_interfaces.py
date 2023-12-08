

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
    name = "IBM.NOS.get_interface_status"
    interface = IGetInterfaces
    pattern_status_up = r'(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(up|down|disabled)\s+(.+)'

    def execute_cli(self):

        interfaces = []
        try:
            v = self.cli("show interface status")
        except self.CLISyntaxError:
            return []
        if v:
            matches1 = re.findall(self.pattern_status_up, v)
            for match1 in matches1:
                ifname = match1[0]
                ifindex = match1[1]
                status = match1[2]
                desc = match1[3]
                a_stat = 'up'
                if status == 'disabled':
                    a_stat = 0
                    status = 0
                if status == 'up':
                    a_stat = 1
                    status = 1
                elif status == 'down':
                    a_stat = 1
                    status = 0
                iface = {
                    "name": ifname,
                    "admin_status": a_stat,
                    "oper_status": status,
                    "description": desc,
                    "type": "physical",
                    "enabled_protocols": [],
                    "snmp_ifindex": ifindex,
                    "subinterfaces": [],
                }
                interfaces += [iface]

        return [{"interfaces": interfaces}]



