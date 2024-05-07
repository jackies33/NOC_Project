

from noc.sa.models.managedobject import ManagedObject
from noc.inv.models.interface import Interface
from noc.inv.models.interfaceprofile import InterfaceProfile
from noc.core.mongo.connection import connect
connect()

target_profile = InterfaceProfile.objects.get(name="dwdm_dom")


for mo in ManagedObject.objects.filter(name__startswith="dwdm"):
      mo_id = int(mo.id)
      for iface in Interface.objects.filter(managed_object=mo_id):
            iface.profile = target_profile
            iface.save()
      mo.save()



for mo in ManagedObject.objects.filter(name="sdc-mus-dwdm"):
      mo_id = int(mo.id)
      for iface in Interface.objects.filter(managed_object=mo_id):
            iface.profile = target_profile
            iface.save()
      mo.save()