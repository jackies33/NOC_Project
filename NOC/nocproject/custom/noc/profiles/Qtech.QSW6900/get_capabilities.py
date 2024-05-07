
# ---------------------------------------------------------------------
# Qtech.QSW6900.get_capabilities
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.sa.profiles.Generic.get_capabilities import Script as BaseScript
from noc.sa.profiles.Generic.get_capabilities import false_on_cli_error


class Script(BaseScript):
    name = "Qtech.QSW6900.get_capabilities"

    rx_lldp = re.compile(r"Global status of LLDP\s+:\s+\S+", re.MULTILINE)

    @false_on_cli_error
    def has_lldp_cli(self):
        """
        Check box has lldp enabled
        """
        r = self.cli("show lldp status")
        match = self.rx_lldp.search(r)
        try:
            match = match[0].split(": ")[1].strip()
        except Exception:
            pass
        result = None
        if match == "Enable":
            result = "lldp"
        return result

