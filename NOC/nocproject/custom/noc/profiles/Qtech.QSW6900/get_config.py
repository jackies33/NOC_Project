# ---------------------------------------------------------------------
# Qtech.QSW6900.get_config
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetconfig import IGetConfig


class Script(BaseScript):
    name = "Qtech.QSW6900.get_config"
    interface = IGetConfig

    def execute_cli(self, **kwargs):
        # Try snmp first
        #
        #
        # See bug NOC-291: http://bt.nocproject.org/browse/NOC-291
        #
        #
        """
        if self.snmp and self.access_profile.snmp_rw
            and TFTP_IP and file_name:
            try:
                # The ConfigCopyProtocol is set to TFTP
                self.snmp.set('1.3.6.1.4.1.9.9.96.1.1.1.1.2.111', 1)
                # Set the SourceFileType to running-config
                self.snmp.set('1.3.6.1.4.1.9.9.96.1.1.1.1.3.111', 4)
                # Set the DestinationFileType to networkfile
                self.snmp.set('1.3.6.1.4.1.9.9.96.1.1.1.1.4.111', 1)
                # Sets the ServerAddress to the IP address of the TFTP server
                self.snmp.set('1.3.6.1.4.1.9.9.96.1.1.1.1.5.111', TFTP_IP)
                # Sets the CopyFilename to your desired file name.
                self.snmp.set('1.3.6.1.4.1.9.9.96.1.1.1.1.6.111', file_name)
                # Sets the CopyStatus to active which starts the copy process.
                self.snmp.set('1.3.6.1.4.1.9.9.96.1.1.1.1.14.111', 1)
                conf_file = open(TFTP_root + '/' + file_name, 'r')
                config = conf_file.read()
                conf_file.close()
                config = self.strip_first_lines(config, 0)
                return self.cleaned_config(config)
            except self.snmp.TimeOutError:
                pass
        """

        # Fallback to CLI
        config = self.cli("show running-config")
        config = self.strip_first_lines(config, 1)
        # Fix Qtech BUG:
        config = config.replace(
            "\n\n                                                                          ", "\n"
        )
        return self.cleaned_config(config)


