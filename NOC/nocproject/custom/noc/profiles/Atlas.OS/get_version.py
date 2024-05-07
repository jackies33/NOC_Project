
# 1.3.6.1.4.1.39433.1.6.1.5.4.1.2 = version OS
# 1.3.6.1.4.1.39433.1.6.1.5.1.1.11 - platform
# 1.3.6.1.4.1.39433.1.6.1.5.1.1.10 - serial_number


# 1.3.6.1.4.1.39433.1.6.1.5.{5} - number of slot in chassis



# ---------------------------------------------------------------------
# Atlas.OS.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion



class Script(BaseScript):
    name = "Atlas.OS.get_version"
    cache = True
    interface = IGetVersion


    def execute_snmp(self, **kwargs):
        r = {}
        try:
            p = None
            v = None
            vendor = "T8"
            platform  = self.snmp.get("1.3.6.1.4.1.39433.1.6.1.5.1.1.11", cached = True)
            #platform = f"{vendor} {platform}"
            version = self.snmp.get("1.3.6.1.4.1.39433.1.6.1.5.4.1.2", cached = True)
            try:
                version = version.split("/")[0].strip()
            except Exception as err:
                pass
            r = {"vendor": vendor, "platform": platform, "version": version}
        except Exception as err:
            print(err)
        return r








        platform, version, image = self.parse_version(v)
            if platform in self.BAD_PLATFORM:
                platform = self.snmp.get(
                    mib["ENTITY-MIB::entPhysicalModelName", 2]
                )  # "Quidway S5628F-HI"
                platform = platform.split()[-1]
                version1 = self.snmp.get(
                    mib["ENTITY-MIB::entPhysicalSoftwareRev", 2]
                )  # like "5.20 Release 2102P01"
                version2 = self.snmp.get(
                    mib["ENTITY-MIB::entPhysicalSoftwareRev", 7]
                )  # "V200R001B02D015SP02"
                version = "%s (%s)" % (version1.split()[0], version2)
            serial = []
            for oid, x in self.snmp.getnext(mib["ENTITY-MIB::entPhysicalSerialNum"]):
                if not x:
                    continue
                serial += [smart_text(x, errors="replace").strip(smart_text(" \x00"))]
            if platform in self.hw_series:
                # series name, fix
                platform = self.fix_platform_name(platform)
            r = {"vendor": "Huawei", "platform": platform, "version": version}
            attributes = {}
            if image:
                r["version"] = "%s (%s)" % (version, image)
                r["image"] = image
            if serial:
                attributes["Serial Number"] = serial[0]
            patch = self.parse_patch()
            if patch:
                attributes["Patch Version"] = patch[0]
            if attributes:
                r["attributes"] = attributes.copy()
            return r