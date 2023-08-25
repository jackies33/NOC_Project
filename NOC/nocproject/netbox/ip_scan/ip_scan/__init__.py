



from extras.plugins import PluginConfig


class IpScanConfig(PluginConfig):
    name = 'ip_scan'
    verbose_name = 'Scan device by ip'
    description = 'Scan device by ip for add new devices'
    version = '0.1.0'
    author = 'Stepanov Evgeniy'
    author_email = 'jacksontur@yandex.ru'


config = IpScanConfig


