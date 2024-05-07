



# ---------------------------------------------------------------------
# Qtech.QSW6900.get_interface_status
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
    name = "Qtech.QSW6900.get_interface_status_ex"
    interface = IGetInterfaceStatusEx

    def execute_snmp(self, interface=None, **kwargs):
        r = []
        # Try SNMP first
        if self.has_snmp():
            try:
                for i, n, status , speed in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.2.2.1.8", "1.3.6.1.4.1.27514.1.1.10.2.10.1.1.1.33"]):
                    iface_name = self.profile.convert_interface_name(n)
                    convert_to_mb = speed * 1000
                    if iface_name:
                        if int(status) == 1:
                            status = True
                            r.append({"interface": iface_name, "oper_status": status,"admin_status":status,
                                      "in_speed":convert_to_mb,"out_speed":convert_to_mb,"full_duplex":True})
                        elif int(status) == 2:
                            status = False
                            r.append({"interface": iface_name, "oper_status": status, "admin_status": status,
                                      "in_speed": convert_to_mb, "out_speed": convert_to_mb,"full_duplex": True})
                return r
            except self.snmp.TimeOutError:
                pass







