

# ---------------------------------------------------------------------
# Vendor: Altas
# OS:     OS
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# import re
# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Atlas.OS"

    requires_netmask_conversion = True
    convert_mac = BaseProfile.convert_mac_to_cisco
