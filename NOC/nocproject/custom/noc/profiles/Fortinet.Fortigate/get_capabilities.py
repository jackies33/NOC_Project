

# ---------------------------------------------------------------------
# Fortinet.Fortigate.get_capabilities
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
    name = "Fortinet.Fortigate.get_capabilities"


    @false_on_cli_error
    def has_lldp_cli(self):
        """
        Check box has lldp enabled
        """

        return "On"
