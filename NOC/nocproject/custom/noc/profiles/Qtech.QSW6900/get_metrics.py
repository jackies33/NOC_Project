
# ---------------------------------------------------------------------
# Qtech.QSW6900.get_metrics
# ---------------------------------------------------------------------
# Copyright (C) 2007-2024 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
from typing import List, Dict, Tuple, Union

# NOC modules
from noc.sa.profiles.Generic.get_metrics import (
    Script as GetMetricsScript,
    metrics,
    ProfileMetricConfig,
    MetricConfig,
)


class Script(GetMetricsScript):
    name = "Qtech.QSW6900.get_metrics"
    always_prefer = "S"


    @metrics(
        ["Interface | Status | Oper",
         "Interface | Status | Admin",
         ],
        volatile=False,
        access="S",  # SNMP version
    )
    def get_interface_status(self, metrics):
        """
        Collect interfaces status metrics
        """

        try:
            metrics = []
            for i, n, s in self.snmp.join(["1.3.6.1.2.1.31.1.1.1.1", "1.3.6.1.2.1.2.2.1.8"]):
                iface_name = self.profile.convert_interface_name(n)
                if iface_name:
                    if int(s) == 1:
                        status = 1
                        metrics.append({"interface": iface_name, "status_oper": status, "status_admin": status})
                    elif int(s) == 2:
                        status = 0
                        metrics.append({"interface": iface_name, "status_oper": status, "status_admin": status})
            for m in metrics:
                if m.get("status_oper") is not None:
                    label_iface = f"noc::interface::{m['interface']}"
                    self.set_metric(
                        id=("Interface | Status | Oper", [label_iface]),
                        labels=[label_iface],
                        value=int(m['status_oper']),
                        multi=True,
                        units="ifaceoper"
                    )
                if m.get("status_admin") is not None:
                    label_iface = f"noc::interface::{m['interface']}"
                    self.set_metric(
                        id=("Interface | Status | Admin", [label_iface]),
                        labels=[label_iface],
                        value=int(m['status_admin']),
                        multi=True,
                        units="ifaceoper"
                    )
        except self.snmp.TimeOutError:
            pass
