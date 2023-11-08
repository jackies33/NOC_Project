

from django.shortcuts import render
from django.views import generic
from .forms import DevicePluginForm
from django.http import HttpResponse
from http import HTTPStatus
from .connect_to_device import CONNECT_DEVICE

class Add_Device_View(generic.TemplateView):
    template_name = 'fast_add_device/fast_add_device.html'
    form_class = DevicePluginForm

    def get_context_data(self, **kwargs):
        con = super().get_context_data(**kwargs)
        con['form'] = self.form_class
        return con

    def get(self, request):
        form = DevicePluginForm
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = DevicePluginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ip_address = form.cleaned_data['ip_address']
            platform = form.cleaned_data['platform'].id
            device_type = form.cleaned_data['device_type'].id
            device_role = form.cleaned_data['device_role'].id
            tenants = form.cleaned_data['tenants'].id
            location = form.cleaned_data['location'].id
            managment = form.cleaned_data['managment']
            device_connect = CONNECT_DEVICE(str(ip_address),int(platform),int(device_type),
                                            int(device_role),int(tenants),int(location),int(managment))
            connecting = device_connect.prepare_for_connection()
            #location_id = form.cleaned_data['location'].id
            #print(data)
            #print(ip_address,platform,device_type,device_role,tenants,location,managment)
            #object_model = DevicesPluginModel.objects.create(**form.cleaned_data)
            #object_model.save()
            return render(request, self.template_name, context={'form': self.form_class, 'response': "True"}, status=HTTPStatus.CREATED)

        else:
            return HttpResponse('Something gone wrong', status=HTTPStatus.BAD_REQUEST)

