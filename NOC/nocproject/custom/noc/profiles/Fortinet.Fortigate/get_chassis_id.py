

# ---------------------------------------------------------------------
# Fortinet.Fortigate.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2011 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.sa.profiles.Generic.get_chassis_id import Script as BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID


class Script(BaseScript):
    name = "Fortinet.Fortigate.get_chassis_id"
    always_prefer = "S"
    interface = IGetChassisID


    def execute_cli(self):
        try:

            self.cli("config global")
            v = self.cli("get hardware nic b-chassis", cached=True)
            matches_mac = re.findall("Permanent_HWaddr\s+\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}", v)
            for mac_f in matches_mac:
                mac = mac_f.split("Permanent_HWaddr")[1].split()[0]
                return {"first_chassis_mac": mac, "last_chassis_mac": mac}
        except Exception as err:
            print(err)
            return  []


        raise self.NotSupportedError()





