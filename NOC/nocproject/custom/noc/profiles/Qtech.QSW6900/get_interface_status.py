
# ---------------------------------------------------------------------
# Qtech.QSW6900.get_interface_status
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfacestatus import IGetInterfaceStatus


class Script(BaseScript):
    name = "Qtech.QSW6900.get_interface_status"
    interface = IGetInterfaceStatus

    rx_interface_status= re.compile(r"^(?P<interface>.+)\s+(?P<status>(up|down))\s+(up|down)", re.MULTILINE)
    rx_interface_status1 = re.compile(r"^(?P<interface>\S+)\s+(?P<status>UP|DOWN)", re.MULTILINE)

    def execute(self, interface=None):
        r = []
        # Try SNMP first
        if self.has_snmp():
            try:
                for i, n, s in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.2.2.1.8"]):
                    iface_name = self.profile.convert_interface_name(n)
                    if iface_name:
                                r.append({"interface": iface_name, "status": int(s) == 1})
                return r
            except self.snmp.TimeOutError:
                pass
                # Fallback to CLI
                cmd = "show interface brief"

                try:
                    c = self.cli(cmd)
                    for match in self.rx_interface_status.finditer(c):
                        iface = self.profile.convert_interface_name(match.group("interface"))
                        r.append({"interface": iface, "status": match.group("status") == "up"})
                except self.CLISyntaxError:
                    pass
                return r


