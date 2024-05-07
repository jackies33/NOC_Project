


# ---------------------------------------------------------------------
# IBM.NOS.get_lldp_neighbors
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetlldpneighbors import IGetLLDPNeighbors
from noc.core.validators import is_int, is_ipv4
from noc.sa.interfaces.base import MACAddressParameter,InterfaceNameParameter


class Script(BaseScript):
    name = "IBM.NOS.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    rx_lldp = re.compile(
        r"^(?P<local_port>\S+)\s+\|\s+\d+\s+\|\s+(?P<remote_id>\S+|.{17})"
        r"\s+\|\s(?P<remote_port>\S+)\s+\|\s+(?P<remote_n>\S+)\s*\|",
        re.MULTILINE,
    )

    rx_mac = re.compile(r"(?:(?:\d|\w){2}[\-\s\:]){5}(?:\d|\w){2}")

    def execute_cli(self):
        r = []
        try:
            v = self.cli("show lldp remote-device | begin LocalPort")
        except self.CLISyntaxError:
            raise self.NotSupportedError()
        if v:
            for match in self.rx_lldp.finditer(v):
                local_port = match.group("local_port")
                remote_chassis_id = match.group("remote_id")
                remote_chassis_id_subtype = 4
                remote_port = match.group("remote_port")
                checking_lenovo_port = re.match(r"^\d{2}$", remote_port)
                if checking_lenovo_port != None:
                    scale_ids = [{"snmp_id": 129, "port_id": 1}, {"snmp_id": 130, "port_id": 2},
                                 {"snmp_id": 131, "port_id": 3}, {"snmp_id": 132, "port_id": 4},
                                 {"snmp_id": 133, "port_id": 5}, {"snmp_id": 134, "port_id": 6},
                                 {"snmp_id": 135, "port_id": 7}, {"snmp_id": 136, "port_id": 8},
                                 {"snmp_id": 137, "port_id": 9}, {"snmp_id": 138, "port_id": 10},
                                 {"snmp_id": 139, "port_id": 11}, {"snmp_id": 140, "port_id": 12},
                                 {"snmp_id": 141, "port_id": 13}, {"snmp_id": 142, "port_id": 14},
                                 {"snmp_id": 143, "port_id": 15}, {"snmp_id": 144, "port_id": 16},
                                 {"snmp_id": 145, "port_id": 17}, {"snmp_id": 146, "port_id": 18},
                                 {"snmp_id": 147, "port_id": 19}, {"snmp_id": 148, "port_id": 20},
                                 {"snmp_id": 149, "port_id": 21}, {"snmp_id": 150, "port_id": 22},
                                 {"snmp_id": 151, "port_id": 23}, {"snmp_id": 152, "port_id": 24},
                                 {"snmp_id": 153, "port_id": 25}, {"snmp_id": 154, "port_id": 26},
                                 {"snmp_id": 155, "port_id": 27}, {"snmp_id": 156, "port_id": 28},
                                 {"snmp_id": 171, "port_id": 43}, {"snmp_id": 172, "port_id": 44},
                                 {"snmp_id": 173, "port_id": 45}, {"snmp_id": 174, "port_id": 46},
                                 {"snmp_id": 175, "port_id": 47}, {"snmp_id": 176, "port_id": 48},
                                 {"snmp_id": 177, "port_id": 49}, {"snmp_id": 178, "port_id": 50},
                                 {"snmp_id": 179, "port_id": 51}, {"snmp_id": 180, "port_id": 52},
                                 {"snmp_id": 185, "port_id": 57}, {"snmp_id": 186, "port_id": 58},
                                 {"snmp_id": 187, "port_id": 59}, {"snmp_id": 188, "port_id": 60},
                                 {"snmp_id": 189, "port_id": 61}, {"snmp_id": 190, "port_id": 62},
                                 {"snmp_id": 191, "port_id": 63}, {"snmp_id": 192, "port_id": 64},
                                 {"snmp_id": 193, "port_id": 65}, {"snmp_id": 194, "port_id": 66}]
                    for id in scale_ids:
                        if str(id["port_id"]) == remote_port:
                            remote_port = str(id["snmp_id"])

                elif checking_lenovo_port == None:
                    pass
                #if "Eth" in remote_port:
                #    remote_port = re.sub(r"Eth", "Et ", remote_port)
                rn = match.group("remote_n")
                remote_port_subtype = 5
                if self.rx_mac.match(remote_port):
                    remote_port = InterfaceNameParameter().clean(remote_port)
                    remote_port_subtype = 3
                elif is_ipv4(remote_port):
                    remote_port_subtype = 4
                elif is_int(remote_port):
                    remote_port_subtype = 7
                if self.rx_mac.match(remote_chassis_id):
                    remote_chassis_id = remote_chassis_id.replace(" ", "-")
                    remote_chassis_id = MACAddressParameter().clean(remote_chassis_id)
                remote_chassis_id_subtype = 4
                remote_port_subtype = 7
                n = {
                    "remote_port": remote_port,
                    "remote_port_subtype": remote_port_subtype,
                    "remote_chassis_id": remote_chassis_id,
                    "remote_chassis_id_subtype": remote_chassis_id_subtype,
                    "remote_system_name": rn,
                }
                i = {"local_interface": local_port, "neighbors": [n]}
                r += [i]
        return r