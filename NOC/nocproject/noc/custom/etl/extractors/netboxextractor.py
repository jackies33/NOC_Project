



import ipaddress
from collections import namedtuple
import pynetbox
import traceback

# NOC modules

from noc.core.etl.extractor.base import BaseExtractor
from noc.core.etl.remotesystem.base import BaseRemoteSystem
from noc.core.etl.models.managedobject import ManagedObject
from noc.core.etl.models.managedobjectprofile import ManagedObjectProfile
from noc.core.etl.models.networksegment import NetworkSegment
from noc.core.etl.models.networksegmentprofile import NetworkSegmentProfile
from noc.core.etl.models.administrativedomain import AdministrativeDomain
from noc.core.etl.models.authprofile import AuthProfile
from noc.core.etl.models.resourcegroup import ResourceGroup
from noc.custom.etl.extractors.classifier_for_extractor import CLASSIFIER
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
        ['4', "nocdwdm", "","","nocdwdm","CgDji.5yLE3>kh7(","","n0cdwdm",""],
    ]


@NBRemoteSystem.extractor
class NBManagedObjectProfileExtractor(BaseExtractor):
    """
    """


    name = "managedobjectprofile"
    model = ManagedObjectProfile
    """
    data = [
        ["2", "EX2200-48P-4G", 25],
        ['3', "NE20E-S2F", 25],
        ['4', "MX204", 25],
        ['5', "MX240", 25],
        ['6', "NetEngine 8000 F1A-8H20Q", 25],
    ]
    """

    def __init__(self, system):
        super(NBManagedObjectProfileExtractor, self).__init__(system)
        self.url = self.url = netbox_url
        self.token = self.token = netbox_api_token
        self.nb = pynetbox.api(url=self.url, token=self.token)
        self.nb.http_session.verify = False

    def iter_data(self, checkpoint=None, **kwargs):
        for type in self.nb.dcim.device_types.all():
            try:
                    if type == None:
                        continue
                    device_type_name = type
                    device_type_id = type.id
                    level = 25
                    yield ManagedObjectProfile(
                       id=str(device_type_id),
                       name=str(device_type_name),
                       level=level,
                    )
            except ValueError:
                print("\n\n\n!!!!failed extract device_type for MO_profile!!!!\n\n\n")
                print('Error:\n', traceback.format_exc(), '\n')
                continue

    def clean(self, row):
        print(row.id,row.name,row.level)
        return row.id,  row.name, row.level

    def extract(self, incremental: bool = False, **kwargs) -> None:
        super(NBManagedObjectProfileExtractor, self).extract()


@NBRemoteSystem.extractor
class NBResourceGroupExtractor(BaseExtractor):
    """
    """


    name = "resourcegroup"
    model = ResourceGroup

    def __init__(self, system):
        super(NBResourceGroupExtractor, self).__init__(system)
        self.url = self.url = netbox_url
        self.token = self.token = netbox_api_token
        self.nb = pynetbox.api(url=self.url, token=self.token)
        self.nb.http_session.verify = False

    def iter_data(self, checkpoint=None, **kwargs):
        try:


            gr_roles = self.nb.tenancy.contact_roles.all()

            for gr_role in gr_roles:
                gr_role_id = gr_role.id
                gr_role_name = gr_role.name
                yield ResourceGroup(
                   id=str(gr_role_id),
                   name=str(gr_role_name),
                   technology="Group"
                )
        except ValueError:
            print("\n\n\n!!!!failed extract tenants for adm_domain!!!!\n\n\n")
            print('Error:\n', traceback.format_exc(), '\n')


    def clean(self, row):
        return row.id,  row.name, row.technology

    def extract(self, incremental: bool = False, **kwargs) -> None:
        super(NBResourceGroupExtractor, self).extract()


@NBRemoteSystem.extractor
class NBAdministrativeDomainExtractor(BaseExtractor):
    """
    """

    name = "administrativedomain"
    model = AdministrativeDomain
    """
    data = [
        ['3', "omsu", None] ,
        ['4', "gku_mo_moc_ikt", None],
    ]
    """

    def __init__(self, system):
        super(NBAdministrativeDomainExtractor, self).__init__(system)
        self.url = self.url = netbox_url
        self.token = self.token = netbox_api_token
        self.nb = pynetbox.api(url=self.url, token=self.token)
        self.nb.http_session.verify = False

    def iter_data(self, checkpoint=None, **kwargs):
        for tenant in self.nb.tenancy.tenants.all():
            try:
                    if tenant == None:
                        continue
                    tenans_name = tenant.name
                    tenans_id = tenant.id

                    yield AdministrativeDomain(
                       id=str(tenans_id),
                       name=str(tenans_name),
                    )
            except ValueError:
                print("\n\n\n!!!!failed extract tenants for adm_domain!!!!\n\n\n")
                print('Error:\n', traceback.format_exc(), '\n')
                continue

    def clean(self, row):
        return row.id,  row.name

    def extract(self, incremental: bool = False, **kwargs) -> None:
        super(NBAdministrativeDomainExtractor, self).extract()

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
                       id=str(device_role_id),
                       parent=str(device_role),
                       name=None,
                       sibling=None,
                       profile="default",
                    )
            except ValueError:
                print("\n\n\n!!!!failed extract device_role for network segment!!!!\n\n\n")
                print('Error:\n', traceback.format_exc(), '\n')
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
                        host_name = str(device.name)
                        if "wap" in host_name:
                            continue
                        self.seen_ip.add(device.primary_ip)
                        netbox_interfaces[device.id] = str(device.primary_ip)
                        host_id = device.id
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
                        custom_filed = dict(device.custom_fields)
                        resource_group = []
                        tg_resource_group_dict = device.custom_fields["TG_Group"]
                        map_resource_group_dict = device.custom_fields["MAP_Group"]
                        name_of_establishmnet = device.custom_fields['Name_of_Establishment']
                        if tg_resource_group_dict != None:
                            tg_resource_group = tg_resource_group_dict["id"]
                            resource_group.append(tg_resource_group)
                        if map_resource_group_dict != None:
                            map_resource_group = map_resource_group_dict["id"]
                            resource_group.append(map_resource_group)
                        classification = CLASSIFIER(device_type,device_role,custom_filed)
                        AuProf = classification.classifier_AuthProf(device_type,device_role)
                        AuthScheme = classification.classifier_AuthScheme(custom_filed)
                        site = device.site.id
                        site = self.nb.dcim.sites.get(id=site)
                        my_address = str(site.physical_address)
                        if name_of_establishmnet != None:
                            my_address = (f'{my_address}\n({name_of_establishmnet})')
                        vc_enable = device.virtual_chassis
                        if vc_enable != None:
                            try:
                                host_name = host_name.split('.')[0]
                            except Exception as err:
                                pass
                        else:
                            pass

                        yield ManagedObject(
                            id=host_id,
                            name=host_name,
                            is_managed = host_status,
                            state=host_status,  # is_managed
                            administrative_domain=AD,  # ID AdministativeDomain
                            pool=pool,  # Pool
                            segment=segment,
                            static_client_groups=[],
                            static_service_groups=resource_group,
                            profile=SAprofile,  # SA Profile
                            object_profile=OP,  # ID Object Profile
                            scheme=AuthScheme,  # AccessType 2 - SSH
                            address=host_ip_address,  # Address
                            description=my_address,
                            tags=[],
                            auth_profile=AuProf,  # auth_profile
                        )
                        print(f'\n\n{ManagedObject}\n\n')
                except ValueError as e:
                            print(f"\n\n{e}\n\nfailed extract ManagedObject!!!\n\n")
                            print('Error:\n', traceback.format_exc(), '\n')
                            continue

        def extract(self, incremental: bool = False, **kwargs) -> None:
              super(NBManagedObjectExtractor, self).extract()




