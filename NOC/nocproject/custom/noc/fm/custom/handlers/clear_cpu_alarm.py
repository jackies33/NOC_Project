
# ---------------------------------------------------------------------
# clear alarm handlers
# ---------------------------------------------------------------------
# Copyright (C) 2007-2022 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

list_of_MO = [
     "kubik-a-2-tsh3","mfmo-p2f1","mfmo-p1f6","mfmo-p1f2","dpmo-asw-011",
     "kubik-g-1-svo","kubik-g-2-msk-dzks",
]

def delete(alarm):
    if str(alarm.alarm_class) == "NOC | PM | Out of Thresholds":
        metric = alarm.vars['metric']
        if str(metric) == "CPU | Usage":
            for mo in list_of_MO:
                if mo == str(alarm.managed_object.name):
                    alarm.clear_alarm('automate clear for useless alarm')









