




# ---------------------------------------------------------------------
# Atlas.OS.get_dom_status
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
    name = "Atlas.OS.get_dom_status"
    interface = IGetDOMStatus

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


    """
    def merge_data(self,list1,list2):
        merged_data = {}
        for item in list1:
            ifname = item['ifname']
            if ifname not in merged_data:
                merged_data[ifname] = []
            merged_data[ifname].append(item)
        for item in list2:
            ifname = item['ifname']
            if ifname not in merged_data:
                merged_data[ifname] = []
            merged_data[ifname].append(item)
        result = []
        for key in merged_data:
            if len(merged_data[key]) > 1:
                merged_dict = {}
                for sub_dict in merged_data[key]:
                    merged_dict.update(
                        {"ifname": sub_dict["ifname"], f"{sub_dict['metric_type']}": sub_dict["value"]})
                result.append(merged_dict)
            else:
                result.extend(merged_data[key])
        return result
    """

    def execute(self, interface=None):
        ifaces = []
        list_for_ports = []
        list_for_sfp = []
        list_members = []
        for snmp in self.snmp.get_tables(["1.3.6.1.4.1.39433.1.4"]):
            n = str(snmp[0])
            v = str(snmp[1])
            value = re.findall("ten\d+", v)#("ten\d+|evstc\d+|emstc\d+", v)
            if value != []:
                value = value[0]
                number_of_slot = n[-1]
                list_members.append(number_of_slot)
        for number_of_slot in list_members:
                for snmp in self.snmp.get_tables([f"1.3.6.1.4.1.39433.1.6.1.3.{number_of_slot}.2"]):#get idex for certain values
                    if "Ln1Pin" in str(snmp[1]) or "Ln1Pout" in str(snmp[1]) or \
                            "Cl1Pin" in str(snmp[1]) or "Cl1Pout" in str(snmp[1]) or \
                            "Ln1InBER" in str(snmp[1]):#collect only for TP interfaces
                        n = str(snmp[0])
                        if "Tidemark" in str(snmp[1]):
                            continue
                        v = str(snmp[1])
                        list_for_ports.append({"index_for_get_value_port": n, "name_for_get_value_port": v})
                    elif "TxT" in str(snmp[1]):#collect only for sfp
                        n = str(snmp[0])
                        v = str(snmp[1])
                        list_for_sfp.append({"index_for_get_value_sfp": n, "name_for_get_value_sfp": v})
                list_for_ports2 = []
                list_for_sfp2 = []
                for index in list_for_ports:
                    interface_type = (re.findall(f"Ln1|Cl1", index['name_for_get_value_port']))[0]
                    metric_type = (re.findall(f"Pin|Pout|InBER", index['name_for_get_value_port']))[0]
                    try:
                        value = self.snmp.get(f"1.3.6.1.4.1.39433.1.6.1.5.{number_of_slot}.2.{index['index_for_get_value_port']}")
                    except Exception:
                        value = None
                    if metric_type == "Pin":
                        metric_type = "optical_rx_dbm"
                    elif metric_type == "Pout":
                        metric_type = "optical_tx_dbm"
                    elif metric_type == "InBER":
                        metric_type = "current_ber"
                    if interface_type == "Ln1":
                        interface_name = f"Network/{number_of_slot}/TP{index['name_for_get_value_port'].split('TP')[1][0]}"
                    elif interface_type == "Cl1":
                        interface_name = f"Client/{number_of_slot}/TP{index['name_for_get_value_port'].split('TP')[1][0]}"

                    list_for_ports2.append({"ifname":interface_name,"iface_type":interface_type,
                                              "metric_type":metric_type,"value":value})
                for index in list_for_sfp:
                    SFP_port_number = index['name_for_get_value_sfp'].split(f"TxT")[0]
                    try:
                        value = self.snmp.get(f"1.3.6.1.4.1.39433.1.6.1.5.{number_of_slot}.2.{index['index_for_get_value_sfp']}")
                    except Exception:
                        value = None
                    if SFP_port_number in self.sfp_map:
                        match_interface_name = self.sfp_map[SFP_port_number]
                        interface_name = f"{match_interface_name[0]}/{number_of_slot}/{match_interface_name[1]}"
                        metric_type = "temp_c"
                    list_for_sfp2.append({"ifname":interface_name,
                                              "metric_type":metric_type,"value":value})
                merged_data = {}
                for item in list_for_ports2:
                    ifname = item['ifname']
                    if ifname not in merged_data:
                        merged_data[ifname] = []
                    merged_data[ifname].append(item)
                for item in list_for_sfp2:
                    ifname = item['ifname']
                    if ifname not in merged_data:
                        merged_data[ifname] = []
                    merged_data[ifname].append(item)
                result = []
                for key in merged_data:
                    if len(merged_data[key]) > 1:
                        merged_dict = {}
                        for sub_dict in merged_data[key]:
                            merged_dict.update(
                                {"ifname": sub_dict["ifname"], f"{sub_dict['metric_type']}": sub_dict["value"]})
                        result.append(merged_dict)
                    else:
                        result.extend(merged_data[key])
                for res in result:
                    temp_c = None
                    current_ber = None
                    optical_rx_dbm = None
                    optical_tx_dbm = None
                    try:
                        interface = res['ifname']
                        optical_rx_dbm = res["optical_rx_dbm"]
                        optical_tx_dbm = res["optical_tx_dbm"]
                    except Exception:
                        continue
                    try:
                        current_ber = res["current_ber"]
                        if current_ber != '' or current_ber == None:
                            #number_float = float(current_ber)
                            #current_ber = '{:.10f}'.format(number_float)
                            current_ber = int(float(current_ber)*1000000000)
                        else:
                            current_ber = None
                    except Exception as err:
                        pass
                    try:
                        temp_c = res["temp_c"]
                        if temp_c != '' or temp_c == None:
                            temp_c = int(float(temp_c)*10)
                        else:
                            temp_c = None
                    except Exception as err:
                        pass
                    if optical_tx_dbm == '':
                        continue
                    else:
                        optical_tx_dbm = int(float(optical_tx_dbm)*10)
                    if optical_rx_dbm == '':
                        continue
                    else:
                        optical_rx_dbm = int(float(optical_rx_dbm)*10)

                    iface = {"interface": interface,
                             "optical_rx_dbm": optical_rx_dbm,
                             "optical_tx_dbm": optical_tx_dbm,
                             'temp_c': temp_c, 'optical_errors_bip_ds':current_ber
                             }
                    ifaces += [iface]

        return ifaces

