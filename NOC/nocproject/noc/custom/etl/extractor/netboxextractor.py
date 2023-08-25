



import ipaddress
from collections import namedtuple
import pynetbox


# NOC modules

from noc.core.etl.extractor.base import BaseExtractor
from noc.core.etl.remotesystem.base import BaseRemoteSystem
from noc.core.etl.models.managedobject import ManagedObject
from noc.core.etl.models.managedobjectprofile import ManagedObjectProfile
from noc.core.etl.models.networksegment import NetworkSegment
from noc.core.etl.models.networksegmentprofile import NetworkSegmentProfile
from noc.core.etl.models.administrativedomain import AdministrativeDomain
from noc.core.etl.models.authprofile import AuthProfile
from noc.custom.etl.extractors.classifier_for_extractor import classifier
from noc.custom.etl.extractors.psql_conn import psql_conn
from noc.custom.etl.engine.my_pass import netbox_url,netbox_api_token

class NBRemoteSystem(BaseRemoteSystem):
    """

        """





@NBRemoteSystem.extractor
class NBAuthProfile(BaseExtractor):
    """
    """

    name = "authprofile"
    model = AuthProfile



    data = [
        ['2', "nocproject", "","","","h#JN0C8b","","nocproject",""],
        ['3', "nocproject1", "","","","h#JN0C8b","","nocpr0ject",""],
    ]



@NBRemoteSystem.extractor
class NBManagedObjectProfileExtractor(BaseExtractor):
    """
    """


    name = "managedobjectprofile"
    model = ManagedObjectProfile

    data = [
        ["2", "EX2200-48P-4G", 25],
        ['3', "NE20E-S2F", 25],
        ['4', "MX204", 25],
        ['5', "MX240", 25],
        ['6', "NetEngine 8000 F1A-8H20Q", 25],
    ]



@NBRemoteSystem.extractor
class NBAdministrativeDomainExtractor(BaseExtractor):
    """
    """

    name = "administrativedomain"
    model = AdministrativeDomain
    data = [
        ['3', "omsu", None] ,
        ['4', "gku_mo_moc_ikt", None],
    ]



@NBRemoteSystem.extractor
class NBNetworkSegmentProfileExtractor(BaseExtractor):
    name = "networksegmentprofile"
    data = [["default", "default"]]
    model = NetworkSegmentProfile


NSRecord = namedtuple(
    "NSRecord", ["id", "name", "parent", "sibling", "profile"]
)




@NBRemoteSystem.extractor
class NBNetworkSegmentExtractor(BaseExtractor):
    """

    """

    name = "networksegment"
    model = NetworkSegment

    def __init__(self, system):
        super(NBNetworkSegmentExtractor, self).__init__(system)
        self.url = self.url = netbox_url
        self.token = self.token = netbox_api_token
        self.nb = pynetbox.api(url=self.url, token=self.token)
        self.nb.http_session.verify = False

    def iter_data(self, checkpoint=None, **kwargs):
        for role in self.nb.dcim.device_roles.all():
            try:
                    if role == None:
                        continue
                    device_role = role.name
                    device_role_id = role.id
                    yield NSRecord(
                       id=device_role_id,
                       parent=device_role,
                       name=None,
                       sibling=None,
                       profile="default",
                    )
            except ValueError:
                print("failed extract ManagedObject")
                continue

    def clean(self, row):
        return row.id,  row.name, row.parent , row.sibling, row.profile

    def extract(self, incremental: bool = False, **kwargs) -> None:
        super(NBNetworkSegmentExtractor, self).extract()




@NBRemoteSystem.extractor
class NBManagedObjectExtractor(BaseExtractor):


        NBRecord = namedtuple("NBRecord", ["id", "name", "ip", 'status'])
        name = "managedobject"
        model = ManagedObject

        def __init__(self,system):
            super(NBManagedObjectExtractor, self).__init__(system)
            # self.containers = {}  # id -> path
            self.ids = set()
            self.seen_name = set()
            self.seen_ids = {}
            self.seen_ip = set()
            self.url = self.url = netbox_url
            self.token = self.token = netbox_api_token
            self.nb = pynetbox.api(url=self.url, token=self.token)
            self.nb.http_session.verify = False

        def iter_data(self, checkpoint=None, **kwargs):
           netbox_interfaces = {}
           for device in self.nb.dcim.devices.all():
                try:
                        if device == None:
                            continue
                        self.seen_ip.add(device.primary_ip)
                        netbox_interfaces[device.id] = str(device.primary_ip)
                        host_id = device.id
                        host_name = device.name
                        host_status = str(device.status)
                        if host_status == 'Active':
                            host_status = 'Managed'
                        elif host_status == 'Offline':
                            host_status = 'Not Managed'
                        else:
                            host_status = 'Managed'
                        ipaddr = netbox_interfaces[device.id]
                        try:
                             host_ip_address = str(ipaddress.ip_interface(ipaddr).ip)
                        except ValueError:
                            print("failed recieve address")
                            continue
                        pool = 'default'
                        device_role = str(device.device_role)
                        device_type = str(device.device_type)
                        AD = device.tenant.id
                        segment = device.device_role.id
                        SAprofile = str(device.platform)
                        OP = device.device_type.id
                        classifierCL = classifier()
                        AuProf = classifierCL.classifier_AuthProf(device_type, device_role)
                        #location = str(device.location)
                        location_id = device.location.id
                        location_name = device.location
                        location_all = self.nb.dcim.locations.get(location_id)
                        parent = location_all.parent
                        location = 'empty'
                        psql = psql_conn()
                        if parent == None:
                            location = str(location_name)
                        elif parent != None:
                            location = str(psql.get_result(location_id))
                        AuthScheme = classifierCL.classifier_AuthScheme(dict(device.custom_fields))
                        yield ManagedObject(
                            id=host_id,
                            name=host_name,
                            is_managed = host_status,
                            state=host_status,  # is_managed
                            administrative_domain=AD,  # ID AdministativeDomain
                            pool=pool,  # Pool
                            segment=segment,
                            static_client_groups=[],
                            static_service_groups=[],
                            profile=SAprofile,  # SA Profile
                            object_profile=OP,  # ID Object Profile
                            scheme=AuthScheme,  # AccessType 2 - SSH
                            address=host_ip_address,  # Address
                            description=location,
                            tags=[],
                            auth_profile=AuProf,  # auth_profile
                        )
                        print(f'\n\n{ManagedObject}\n\n')
                except ValueError as e:
                            print(f"\n\n{e}\n\nfailed extract ManagedObject!!!\n\n")
                            continue

        def extract(self, incremental: bool = False, **kwargs) -> None:
              super(NBManagedObjectExtractor, self).extract()




