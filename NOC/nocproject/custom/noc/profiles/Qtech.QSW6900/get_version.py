



# ---------------------------------------------------------------------
# Qtech.QSW6900.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re


# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion



class Script(BaseScript):
    name = "Qtech.QSW6900.get_version"
    cache = True
    interface = IGetVersion


    def execute(self, **kwargs):
        r = {}
        try:
            output_version = self.cli("show version")
            platform = re.findall(f"System description\s+:\s+.+\n", output_version)[0].split(": ")[1].split("\n")[0]
            version = re.findall(f"System software version\s+:\s+.+\n", output_version)[0].split(": ")[1].split("\n")[0]
            vendor = "Qtech"
            r = {"vendor": vendor, "platform": platform, "version": version}
        except Exception as err:
            print(err)
        return r



