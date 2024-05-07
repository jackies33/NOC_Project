
# ---------------------------------------------------------------------
# Atlas.OS.get_inventory
# ---------------------------------------------------------------------
# Copyright (C) 2007-2022 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
from itertools import groupby

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinventory import IGetInventory
from noc.core.validators import is_int


class Script(BaseScript):
    name = "Atlas.OS.get_inventory"
    interface = IGetInventory

    TYPE_MAP = {
        "CHASSIS": "CHASSIS",
        "PEM": "PEM",
        "POWER SUPPLY": "PEM",
        "PDM": "PDM",  # Power Distribution Module
        "PSU": "PSU",
        "ROUTING ENGINE": "RE",
        "AFEB": "AFEB",
        "CB": "SCB",
        "MGMT BRD": "MGMT",
        "FPM BOARD": "FPM",  # Front Panel Display
        "QXM": "QXM",  # QX chip (Dense Queuing Block)
        "CPU": "CPU",  # MPC CPU
        "FPC": "FPC",
        "MPC": "FPC",
        "MIC": "MIC",
        "PIC": "PIC",
        "XCVR": "XCVR",
        "FTC": "FAN",
        "FAN TRAY": "FAN",
    }

    sfp_map = {
        "SFP1": ("Client", "TP1"),
        "SFP2": ("Client", "TP2"),
        "SFP3": ("Client", "TP3"),
        "SFP4": ("Client", "TP4"),
        "SFP5": ("Client", "TP5"),
        "SFP6": ("Client", "TP6"),
        "SFP7": ("Network", "TP1"),
        "SFP8": ("Network", "TP2"),
        "SFP9": ("Network", "TP3"),
        "SFP10": ("Network", "TP4"),
        "SFP11": ("Network", "TP5"),
        "SFP12": ("Network", "TP6"),
    }

    def execute_snmp(self, interface=None):
        objects = []
        list_members = []
        list_for_discovery = []
        for snmp in self.snmp.get_tables(["1.3.6.1.4.1.39433.1.4"]):
            n = str(snmp[0])
            v = str(snmp[1])
            value = re.findall("ten\d+", v)  # ("ten\d+|evstc\d+|emstc\d+", v)
            if value != []:
                value = value[0]
                number_of_slot = n[-1]
                list_members.append(number_of_slot)
        for number_of_slot in list_members:
            for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.3.{number_of_slot}.1"]):  # get idex for certain values
                if "Description" in str(snmp[1]):
                    sfp_name = snmp[1].split("Description")[0]
                    inv_type = "sfp_description"
                    sfp_index = snmp[0]
                    if sfp_name in self.sfp_map:
                        match_interface_name = self.sfp_map[sfp_name]
                        iface = f"{match_interface_name[0]}/{number_of_slot}/{match_interface_name[1]}"
                        list_for_discovery.append({"sfp_name": sfp_name, "inv_type": inv_type,
                                               "sfp_index": sfp_index, "iface": iface})
                elif "Vendor" in str(snmp[1]):
                    sfp_name = snmp[1].split("Vendor")[0]
                    inv_type = "sfp_vendor"
                    sfp_index = snmp[0]
                    if sfp_name in self.sfp_map:
                        match_interface_name = self.sfp_map[sfp_name]
                        iface = f"{match_interface_name[0]}/{number_of_slot}/{match_interface_name[1]}"
                        list_for_discovery.append({"sfp_name": sfp_name, "inv_type": inv_type,
                                                   "sfp_index": sfp_index, "iface": iface})
                elif "PtNumber" in str(snmp[1]):
                    sfp_name = snmp[1].split("PtNumber")[0]
                    inv_type = "sfp_ptnumber"
                    sfp_index = snmp[0]
                    if sfp_name in self.sfp_map:
                        match_interface_name = self.sfp_map[sfp_name]
                        iface = f"{match_interface_name[0]}/{number_of_slot}/{match_interface_name[1]}"
                        list_for_discovery.append({"sfp_name": sfp_name, "inv_type": inv_type,
                                                   "sfp_index": sfp_index, "iface": iface})
                elif "SrNumber" in str(snmp[1]):
                    sfp_name = snmp[1].split("SrNumber")[0]
                    inv_type = "sfp_srnumber"
                    sfp_index = snmp[0]
                    if sfp_name in self.sfp_map:
                        match_interface_name = self.sfp_map[sfp_name]
                        iface = f"{match_interface_name[0]}/{number_of_slot}/{match_interface_name[1]}"
                        list_for_discovery.append({"sfp_name": sfp_name, "inv_type": inv_type,
                                                   "sfp_index": sfp_index, "iface": iface})
            for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.5.{number_of_slot}.1"]):  # get values
                for match_dict in list_for_discovery:
                    if int(snmp[0]) == int(match_dict["sfp_index"]):
                        match_dict.update({"value":str(snmp[1].strip())})
            merged_data = {}
            for item in list_for_discovery:
                ifname = item['iface']
                if ifname not in merged_data:
                    merged_data[ifname] = []
                merged_data[ifname].append(item)
            result = []
            for key in merged_data:
                if len(merged_data[key]) > 1:
                    merged_dict = {}
                    for sub_dict in merged_data[key]:
                        merged_dict.update(
                            {"iface": sub_dict["iface"], f"{sub_dict['inv_type']}": sub_dict["value"],
                             "sfp_name": sub_dict["sfp_name"],"sfp_index": sub_dict["sfp_index"]})
                    result.append(merged_dict)
                else:
                    result.extend(merged_data[key])
            #t, number = self.get_type(type_name)
            for r in result:
                        type_name = "XCVR"
                        obj = {
                            "type": type_name,
                            "number":str(r['iface']),
                            "vendor": str(r['sfp_vendor']),
                            "serial": str(r['sfp_srnumber']),
                            "description": str(r['sfp_description']),
                            "part_no": str(r['sfp_ptnumber']),
                            "revision": '',
                            "data": '',
                        }
                        objects.append(obj)
        return objects


    def get_type(self, name):
        name = name.upper()
        n = name.split()
        if is_int(n[-1]):
            number = n[-1]
            name = " ".join(n[:-1])
        else:
            number = None
        return self.TYPE_MAP.get(name), number

