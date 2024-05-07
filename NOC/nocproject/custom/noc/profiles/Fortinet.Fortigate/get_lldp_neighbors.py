


# ---------------------------------------------------------------------
# Fortinet.Fortigate.get_lldp_neighbors
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

    name = "Fortinet.Fortigate.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    rx_lp = re.compile(r"(?P<id_lldp>\d+)\s+port.txt:\s+(?P<local_port>\S+)", re.MULTILINE)
    rx_ch_id = re.compile(r"(?P<id_lldp>\d+)\s+chassis.data:\s+(?P<ch_id>\S+)")
    rx_rem_port = re.compile(r"(?P<id_lldp>\d+)\s+port.id.data:\s+(?P<rem_p_id>\S+)")
    rx_rem_ch_name = re.compile(r"(?P<id_lldp>\d+)\s+system.name.data:\s+(?P<r_ch_name>\S+)")

    def execute_cli(self):
        r = []
        try:
            self.cli("config vdom")
            self.cli("edit root")
            v = self.cli("diagnose lldprx port neighbor details")
        except self.CLISyntaxError:
            raise self.NotSupportedError()
        if v:

                r = []
                temp_n = []

                matches_lp = self.rx_lp.finditer(v)
                matches_ch_id = self.rx_ch_id.finditer(v)
                matches_rem_p_id = self.rx_rem_port.finditer(v)
                matches_rem_ch_name = self.rx_rem_ch_name.finditer(v)

                for match in matches_lp:
                    local_port = match.group("local_port")
                    id_lldp = match.group("id_lldp")
                    temp_n.append({"id_lldp": id_lldp, "local_port": local_port})

                for match in matches_ch_id:
                    id_lldp = match.group("id_lldp")
                    rem_ch_id = match.group("ch_id")
                    for t in temp_n:
                        if t['id_lldp'] == id_lldp:
                            t.update({"ch_id": rem_ch_id})

                for match in matches_rem_p_id:
                    id_lldp = match.group("id_lldp")
                    remote_port = match.group("rem_p_id")
                    for t in temp_n:
                        if t['id_lldp'] == id_lldp:
                            t.update({"remote_port": remote_port})

                for match in matches_rem_ch_name:
                    id_lldp = match.group("id_lldp")
                    remote_ch_name = match.group("r_ch_name")
                    if ".tech.mosreg.ru" in remote_ch_name:
                        remote_ch_name = remote_ch_name.split(".tech.mosreg.ru")[0]
                    for t in temp_n:
                        if t['id_lldp'] == id_lldp:
                            t.update({"remote_chassis_name": remote_ch_name})

                for t in temp_n:
                    remote_port = t["remote_port"]
                    remote_chassis_id = t["ch_id"]
                    rn = t["remote_chassis_name"]
                    finder_mac = None
                    try:
                        finder_mac = re.findall(r'\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}', remote_port)[0]
                    except Exception as err:
                        print(err)
                    if finder_mac != None:
                        rem_port_subtype = 3
                    else:
                        rem_port_subtype = 7
                    local_port = t["local_port"]
                    #if "ha" in local_port:
                    #    print("ha")
                    #    #continue
                    #else:
                    n = {
                        "remote_port": remote_port,
                        "remote_port_subtype": rem_port_subtype,
                        "remote_chassis_id": remote_chassis_id,
                        "remote_chassis_id_subtype": 4,
                        "remote_system_name": rn,
                    }
                    i = {"local_interface": local_port, "neighbors": [n]}
                    r += [i]
        return r



