

from django import forms
from ipam.formfields import IPNetworkFormField
#from django.core.validators import RegexValidator
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from dcim.models.sites import Location
from dcim.models.racks import Rack
from dcim.models.devices import Platform,DeviceType,DeviceRole
from tenancy.models.tenants import Tenant
#from ipam.forms import IPAddressForm

class DevicePluginForm(NetBoxModelForm):

        choices_management = [(1, 'Active'), (2, 'Offline')]
        #ip_address = forms.GenericIPAddressField(protocol='IPv4')
        ip_address = IPNetworkFormField(required=True,label='ip address')#help_text='prefix form "0.0.0.0/0"',)
        platform = DynamicModelChoiceField(required=True,label='platform',queryset = Platform.objects.all())
        device_type = DynamicModelChoiceField(required=True,label='device type',queryset=DeviceType.objects.all())
        device_role = DynamicModelChoiceField(required=True,label='device role',queryset=DeviceRole.objects.all())
        tenants = DynamicModelChoiceField(required=True,label='tenants',queryset=Tenant.objects.all())
        location = DynamicModelChoiceField(required=True,label='location',queryset = Location.objects.all())
        racks = DynamicModelChoiceField(required=False,label='rack',queryset = Rack.objects.all())
        managment = forms.ChoiceField(required=True,label='managment',choices=choices_management)

        class Meta:
            model = Location
            fields = ['ip_address','platform','device_type','device_role','tenants','location','racks','managment']

"""
class RackForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label='location')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['racks'].queryset = Rack.objects.filter(location=self.instance.location)
        else:
            self.fields['racks'].queryset = Rack.objects.none()

    class Meta:
        model = Rack
        fields = ['location', 'racks']
"""