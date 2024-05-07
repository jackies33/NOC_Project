

# ---------------------------------------------------------------------
# Huawei.VRP.get_dom_status
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetdomstatus import IGetDOMStatus



class Script(BaseScript):
    name = "Huawei.VRP.get_dom_status"
    interface = IGetDOMStatus

    rx_port = re.compile(r"Port (?P<port>\S+\d+) transceiver diagnostic information:")

    ne_map = {"tx power": "tx_power", "rx power": "rx_power"}
    ar_map = {
        "current tx power(dbm)": "tx_power",
        "current rx power(dbm)": "rx_power",
        "bias current(ma)": "current",
        "temperature()": "temp",
        "voltage(v)": "voltage",
    }

    def parse_ports(self, s):
        match = self.rx_port.search(s)
        if match:
            port = match.group("port")
            obj = match.groupdict()
            return port, obj, s[match.end() :]
        else:
            return None



    def execute_ne(self, interface=None):

            r = []
            cmd = "display interface phy-option"
            try:
                c = self.cli(cmd)
                print(c)
                output = re.findall(r"(GigabitEthernet\d+\/\d+\/\d+)[\s\S]*?Rx Power:\s*(-?\d+\.\d+)[\s\S]*?Tx Power:\s*(-?\d+\.\d+)",c)
                for o in output:
                    iface = {"interface": re.findall(r"(GigabitEthernet\d+\/\d+\/\d+)", o[0])[0]}
                    iface["optical_rx_dbm"] = float(re.findall(r"-?\d+\.\d+", o[1])[0])
                    iface["optical_tx_dbm"] = float(re.findall(r"-?\d+\.\d+", o[2])[0])
                    r += [iface]

            except self.CLISyntaxError:
                return []

            return r

    def execute(self, interface=None):

            r = []
            cmd = "display interface phy-option"
            try:
                c = self.cli(cmd)
                print(c)
                output = re.findall(r"(GigabitEthernet\d+\/\d+\/\d+)[\s\S]*?Rx Power:\s*(-?\d+\.\d+)[\s\S]*?Tx Power:\s*(-?\d+\.\d+)",c)
                for o in output:
                    iface = {"interface": re.findall(r"(GigabitEthernet\d+\/\d+\/\d+)", o[0])[0]}
                    iface["optical_rx_dbm"] = float(re.findall(r"-?\d+\.\d+", o[1])[0])
                    iface["optical_tx_dbm"] = float(re.findall(r"-?\d+\.\d+", o[2])[0])
                    r += [iface]

            except self.CLISyntaxError:
                return []

            return r
