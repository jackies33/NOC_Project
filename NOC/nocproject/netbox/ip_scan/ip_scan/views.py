

from django.shortcuts import render,redirect
from .forms import IpAddressForm
from .connect_to_device import connect_handler_to_device


def ip_address(request):
          form = IpAddressForm(request.POST)
          if form.is_valid():
                 ip_address = form.cleaned_data['ip_address']
                 #manufacturer = form.cleaned_data['manufacturer']
                 platform = form.cleaned_data['platform']
                 device_type = form.cleaned_data['device_type']
                 #site_name = form.cleaned_data['site_name']
                 location = form.cleaned_data['locations']
                 location_add = form.cleaned_data['locations_add']
                 device_role = form.cleaned_data['device_role']
                 tenants = form.cleaned_data['tenants']
                 management = form.cleaned_data['management']
                 print('its views!!!')
                 finally_result = connect_handler_to_device(ip_address,
                                                            #int(manufacturer) ,
                                                            int(platform),
                                                            int(device_type),
                                                            #int(site_name),
                                                            int(location),
                                                            location_add,
                                                            int(device_role),
                                                            int(tenants),
                                                            int(management),
                 )
                 form = IpAddressForm()
                 #print(ip_address,manufacturer, site_name, device_role, tenants)
                 if finally_result == True:
                     return
                 return redirect(request.META.get('HTTP_REFERER'))


          else:
             form = IpAddressForm()
          return render(request, 'ip_address.html', {'form': form})





