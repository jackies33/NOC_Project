
# ---------------------------------------------------------------------
# HP.ProCurve.get_portchannel
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetportchannel import IGetPortchannel


class Script(BaseScript):
    name = "IBM.NOS.get_portchannel"
    interface = IGetPortchannel

    rx_trunk = re.compile(
        r"^\s*(?P<port>\S+)\s+\|.+?\|\s+(?P<trunk>\S+)\s+(?P<type>(\S+)?$)", re.MULTILINE
    )

    def execute(self):
        r = []
        # Get trunks
        trunks = {}
        trunk_types = {}
        try:
             v = self.cli("show PortChannel information")
        except self.CLISyntaxError:
            return []
        pc_regex = re.compile(r"PortChannel (\d+): Enabled\nProtocol - LACP\nPort State:\n((?:\s+\w+: .+\n)+)",
                              re.MULTILINE)

        matches = pc_regex.findall(v)
        for match in matches:
            port_number, port_data = match
            pred_data = port_data.strip()
            r += [
                {
                    "interface": f"Port-Channel{port_number}",
                    "members": re.findall(r'EXT\d+|INTA\d+', pred_data),
                    "type": "L",
                }
            ]
        return r