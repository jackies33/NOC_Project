


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
from noc.sa.interfaces.igetinterfacestatus import IGetInterfaceStatus


class Script(BaseScript):
    name = "IBM.NOS.get_interface_status"
    interface = IGetInterfaceStatus
    pattern_status_up = r'(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(up|down|disabled)\s+(.+)'
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
                if status == 'disabled':
                    status = False
                if status == 'up':
                    status = True
                elif status == 'down':
                    status == False
                r += [
                        {"interface": ifname, "status": status == 1}
                ]
        return r



