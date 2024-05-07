

# ---------------------------------------------------------------------
# Cisco.NXOS.get_lldp_neighbors
# ---------------------------------------------------------------------
# Copyright (C) 2007-2022 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetlldpneighbors import IGetLLDPNeighbors
from noc.sa.interfaces.base import MACAddressParameter
from noc.core.validators import is_int, is_ipv4
from noc.core.lldp import (
    LLDP_PORT_SUBTYPE_MAC,
    LLDP_PORT_SUBTYPE_NETWORK_ADDRESS,
    LLDP_PORT_SUBTYPE_LOCAL,
    LLDP_CHASSIS_SUBTYPE_MAC,
    LLDP_PORT_SUBTYPE_UNSPECIFIED,
    LLDP_CAP_OTHER,
    LLDP_CAP_REPEATER,
    LLDP_CAP_BRIDGE,
    LLDP_CAP_WLAN_ACCESS_POINT,
    LLDP_CAP_ROUTER,
    LLDP_CAP_TELEPHONE,
    LLDP_CAP_DOCSIS_CABLE_DEVICE,
    LLDP_CAP_STATION_ONLY,
    lldp_caps_to_bits,
)


class Script(BaseScript):
    name = "Cisco.NXOS.get_lldp_neighbors"
    interface = IGetLLDPNeighbors

    rx_summary_split = re.compile(r"^Device ID.+?\n", re.MULTILINE | re.IGNORECASE)
    rx_s_line = re.compile(r"^[\S+\s]*(?P<local_if>(?:Fa|Gi|Te|Eth|mgmt)\d+[\d/\.]*)\s+.+$")
    rx_chassis_id = re.compile(r"^Chassis id:\s*(?P<id>\S+)", re.MULTILINE | re.IGNORECASE)
    rx_remote_port = re.compile(r"^Port id:\s*(?P<remote_if>.+?)\s*$", re.MULTILINE | re.IGNORECASE)
    rx_enabled_caps = re.compile(
        r"^Enabled Capabilities:\s*(?P<caps>\S*)\s*$", re.MULTILINE | re.IGNORECASE
    )
    rx_sys_desc_lenovo = re.compile(r"^System Description:\s*(?P<system_descr>Lenovo Flex System Fabric EN4093R 10Gb Scalable Switch)", re.MULTILINE | re.IGNORECASE)
    rx_system = re.compile(r"^System Name:\s*(?P<name>\S+)", re.MULTILINE | re.IGNORECASE)
    rx_mac = re.compile(r"^[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}$")

    def execute_cli(self):
        r = []
        try:
            v = self.cli("show lldp neighbors")
        except self.CLISyntaxError:
            raise self.NotSupportedError()
        if v.startswith("%"):
            # % LLDP is not enabled
            return []
        v = self.rx_summary_split.split(v)[1]
        lldp_interfaces = []
        # Get LLDP interfaces with neighbors
        for ll in v.splitlines():
            ll = ll.strip()
            if not ll:
                break
            match = self.rx_s_line.match(ll)
            if not match:
                continue
            lldp_interfaces += [match.group("local_if")]
        # Get LLDP neighbors
        for local_if in lldp_interfaces:
            i = {"local_interface": local_if, "neighbors": []}
            # Get neighbors details
            try:
                v = self.cli("show lldp neighbors interface %s detail" % local_if)
            except self.CLISyntaxError:
                # Found strange CLI syntax on Catalyst 4900
                # Allow ONLY interface name or "detail"
                # Need testing...
                raise self.NotSupportedError()
            #Get description of system name for Lenovo(EXCEPTION!!!!)))
            remote_port = None
            match = self.rx_sys_desc_lenovo.search(v)
            if match != None:
                remote_device_type = match.group("system_descr")
                if remote_device_type == "Lenovo Flex System Fabric EN4093R 10Gb Scalable Switch":
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
                    # Get remote port
                    match = self.rx_remote_port.search(v)
                    remote_port = match.group("remote_if")
                    for id in scale_ids:
                        if str(id["port_id"]) == remote_port:
                            remote_port = str(id["snmp_id"])
                            n = {
                                "remote_port": remote_port,

                            }

                        else:
                            pass
                else:
                    pass
            elif match == None:
                pass
            else:
                pass
            # Get remote port
            match = self.rx_remote_port.search(v)
            if remote_port == None:
                remote_port = match.group("remote_if")
                remote_port_subtype = LLDP_PORT_SUBTYPE_UNSPECIFIED
            elif remote_port != None:
                pass
            if self.rx_mac.match(remote_port):
                # Convert MAC to common form
                remote_port = MACAddressParameter().clean(remote_port)
                remote_port_subtype = LLDP_PORT_SUBTYPE_MAC
            elif is_ipv4(remote_port):
                remote_port_subtype = LLDP_PORT_SUBTYPE_NETWORK_ADDRESS
            elif is_int(remote_port):
                remote_port_subtype = LLDP_PORT_SUBTYPE_LOCAL
            n = {
                "remote_port": remote_port,
                "remote_port_subtype": remote_port_subtype,
                "remote_chassis_id_subtype": LLDP_CHASSIS_SUBTYPE_MAC,
            }
            # Get chassis id
            match = self.rx_chassis_id.search(v)
            if not match:
                continue
            n["remote_chassis_id"] = match.group("id")
            # Get capabilities
            cap = 0
            match = self.rx_enabled_caps.search(v)
            if match:
                cap = lldp_caps_to_bits(
                    match.group("caps").strip().split(","),
                    {
                        "o": LLDP_CAP_OTHER,
                        "p": LLDP_CAP_REPEATER,
                        "b": LLDP_CAP_BRIDGE,
                        "w": LLDP_CAP_WLAN_ACCESS_POINT,
                        "r": LLDP_CAP_ROUTER,
                        "t": LLDP_CAP_TELEPHONE,
                        "c": LLDP_CAP_DOCSIS_CABLE_DEVICE,
                        "s": LLDP_CAP_STATION_ONLY,
                        "n/a": 0,
                    },
                )
            n["remote_capabilities"] = cap
            # Get remote chassis id
            match = self.rx_system.search(v)
            if match:
                n["remote_system_name"] = match.group("name")
            i["neighbors"] += [n]
            r += [i]
        return r