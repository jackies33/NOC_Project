
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetdict import IGetDict
# Python modules
import re


class Script(BaseScript):
    name = "Juniper.JUNOS.get_virtual_chassis"
    cache = True
    interface = IGetDict

    # """

    def execute_cli(self):
        v = self.cli("show virtual-chassis")
        find = re.findall(r'\(FPC \d+\)  (?:Prsnt|Mismatch)    \S+', v)
        result = {}

        for target in find:
            member = re.findall(r"\(FPC \d+\)", target)[0]
            if "Mismatch" in target:
                sn = target.split("Mismatch    ")[1]
                target0 = f"\nAlarm! Member {member} S/N:{sn} is DOWN"
                print(f"\nAlarm! Member {member} S/N:{sn} is DOWN")
                membsn = f'member-{member}-s/n {sn}'
                result.update({membsn: "is DOWN"})
                return result
            elif "Prsnt" in target:
                sn = target.split("Prsnt    ")[1]
                target0 = f"\nMember {member} S/N:{sn} is UP"
                print(f"\nMember {member} S/N:{sn} is UP")
                membsn = f'member-{member}-s/n {sn}'
                result.update({membsn: "is UP"})
        return result

    """
    def execute_cli(self):
        v = self.cli("show virtual-chassis")
        find = re.findall(r'\(FPC \d+\)  (?:Prsnt|Mismatch)    \S+', v)
        result = []
        for target in find:
            member = re.findall(r"\(FPC \d+\)", target)[0]
            if "Mismatch" in target:
                sn = target.split("Mismatch    ")[1]
                result.append(f"\nAlarm! Member {member} S/N:{sn} is DOWN")
                print(f"\nAlarm! Member {member} S/N:{sn} is DOWN")
            elif "Prsnt" in target:
                sn = target.split("Prsnt    ")[1]
                result.append(f"\nMember {member} S/N:{sn} is UP")
                print(f"\nMember {member} S/N:{sn} is UP")

        return result        
    """

