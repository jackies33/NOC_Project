
# ---------------------------------------------------------------------
# Juniper.JUNOS.get_dom_status
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetdomstatus import IGetDOMStatus


class Script(BaseScript):
    name = "Juniper.JUNOS.get_dom_status"
    interface = IGetDOMStatus


    def execute(self, interface=None):
        r = []
        cmd = "show interfaces diagnostics optics"
        try:
            c = self.cli(cmd)
            output = re.findall(r"Physical interface:.+\n.+\n.+\n.+\n.+\n.+", c)
            for o in output:
                try:
                    iface = {"interface": re.findall(r"(Physical interface:.+)", o)[0].split("Physical interface: ")[1]}
                    iface["optical_rx_dbm"] = float(re.findall(r"Laser output power.+", o)[0].split("/ ")[1].split(" dBm")[0])
                    iface["optical_tx_dbm"] = float(re.findall(r"Laser receiver power.+", o)[0].split("/ ")[1].split(" dBm")[0])
                    iface["voltage_v"] = None
                    iface["current_ma"] = None
                    iface["temp_c"] = None
                    r += [iface]
                except Exception as err:
                    print(err)
                    continue
        except self.CLISyntaxError:
            return []
        return r

