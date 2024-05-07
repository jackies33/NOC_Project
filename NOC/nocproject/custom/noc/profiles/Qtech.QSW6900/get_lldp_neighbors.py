



# ---------------------------------------------------------------------
# Qtech.QSW6900.get_lldp_neighbors
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetlldpneighbors import IGetLLDPNeighbors



class Script(BaseScript):
    name = "Qtech.QSW6900.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    rx_lldp = re.compile(
        r"(?P<local_port>LLDP neighbor-information of port \[.+\])"
        r"(?:(?!LLDP neighbor-information of port \[).)+?"
        r"(?P<chassis_id>Chassis ID\s+:\s+\S+)"
        r".+?"
        r"(?P<system_name>System name\s+:\s+\S+)"
        r".+?"
        r"(?P<remote_port>Port ID\s+:\s+.+\n)",
        re.MULTILINE |
        re.DOTALL
    )


    def execute_cli(self):
        r = []
        try:
            v = self.cli("show lldp neighbors detail")
        except self.CLISyntaxError:
            raise self.NotSupportedError()
        if v:
            lldp_blocks = v.split("LLDP neighbor-information of port [")[1:]
            for block in lldp_blocks:
                    match = self.rx_lldp.search("LLDP neighbor-information of port [" + block)
                    local_port = match.group("local_port").split("[")[1].split("]")[0]
                    remote_chassis_id = match.group("chassis_id").split(": ")[1].strip()
                    remote_system_name = match.group("system_name").split(": ")[1].strip()
                    if ".tech.mosreg.ru" in remote_system_name:
                        remote_system_name = remote_system_name.split(".tech.mosreg.ru")[0]
                    elif ".tech.mosreg.r" in remote_system_name:
                        remote_system_name = remote_system_name.split(".tech.mosreg.r")[0]
                    remote_port = match.group("remote_port").split(": ")[1].split("\n")[0]

                    remote_port_subtype = 7
                    n = {
                        "remote_port": remote_port,
                        "remote_port_subtype": remote_port_subtype,
                        "remote_chassis_id": remote_chassis_id,
                        "remote_system_name": remote_system_name,
                    }
                    i = {"local_interface": local_port, "neighbors": [n]}
                    r += [i]
        return r

