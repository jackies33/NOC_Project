# ---------------------------------------------------------------------
# Vendor: Qtech
# OS:     QSW6900
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Qtech.QSW6900"

    pattern_username = rb"^(Username\(1-32 chars\)|[Ll]ogin):"
    pattern_password = rb"^Password(\(1-16 chars\)|):"
    pattern_more = [
        (
            rb"^\.\.\.\.press ENTER to next line, CTRL_C to break, other key "
            rb"to next page\.\.\.\.",
            b" ",
        ),
        (rb"^Startup config in flash will be updated, are you sure\(y/n\)\? \[n\]", b"y"),
        (rb"^ --More-- $", b" "),
        (rb"^Confirm to overwrite current startup-config configuration", b"\ny\n"),
        (rb"^Confirm to overwrite the existed destination file?", b"\ny\n"),
        (rb"^Begin to receive file, please wait", b" "),
        (rb"#####", b" "),
    ]
    pattern_unprivileged_prompt = rb"^\S+>"
    pattern_syntax_error = (
        rb"% (Unrecognized command, and error|Invalid input) detected at "
        rb"'\^' marker.|% Ambiguous command:|interface error!|Incomplete "
        rb"command"
    )
    #    command_disable_pager = "terminal datadump"
    command_super = b"enable"
    command_enter_config = "configure"
    command_leave_config = "end"
    command_exit = "quit"
    command_save_config = "copy running-config startup-config"
    pattern_prompt = rb"^\S+#"
    rogue_chars = [
        re.compile(rb"\s*\x1b\[74D\s+\x1b\[74D"),
        re.compile(rb"\s*\x1b\[74D\x1b\[K"),
        b"\r",
    ]
    config_tokenizer = "indent"
    config_tokenizer_settings = {"line_comment": "!"}


    map_interfaces = {
        "TF": "TFGigabitEthernet",
        "Hu": "HundredGigabitEthernet",
        "Ag": "AggregatePort",
        "Lo": "Loopback",
        "Ot": "OverlayTunnel",
        "Vl": "VLAN",
        "Mg": "Mgmt"
    }

    def convert_interface_name(self,interface):
        try:
            interface_find = re.findall(r'\b([a-zA-Z]+)\d',interface)[0]
        except Exception:
            return interface
        if len(interface_find)==2:
            iface_type = interface[:2]
            for key, value in self.map_interfaces.items():
                if key == iface_type:
                    number = interface.split(f"{iface_type}")[1]
                    interface = f"{value} {number}"
                    return interface
        else:
            return interface




