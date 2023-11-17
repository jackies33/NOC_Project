
# ----------------------------------------------------------------------
# Juniper.JUNOSCustoM.get_metrics
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

import re

# NOC modules
from noc.sa.profiles.Generic.get_metrics import Script as GetMetricsScript, metrics


class Script(GetMetricsScript):
    name = "Juniper.JUNOSCustoM.get_metrics"

    @metrics(
        ["Environment | Stack"],
        has_capability="Environment | Stack",
        volatile=False,
    )
    def execute_cli(self):
        v = self.cli("show virtual-chassis")
        find = re.findall(r'\(FPC \d+\)  (?:Prsnt|Mismatch)    \S+', v)
        try:
            for target in find:
                member = re.findall(r"\(FPC \d+\)", target)[0]
                if "Mismatch" in target:
                    sn = target.split("Mismatch    ")[1]
                    print(f"\nAlarm! Member {member} S/N:{sn} is DOWN")
                    self.set_metric(id=("Environment | Stack", None), value=int(1[f"\nMember {member} S/N:{sn} is DOWN"]))
                elif "Prsnt" in target:
                    sn = target.split("Prsnt    ")[1]
                    print(f"\nMember {member} S/N:{sn} is UP")
                    self.set_metric(id=("Environment | Stack", None), value=int(0[f"\nMember {member} S/N:{sn} is UP"]))
        except Exception:
                pass


